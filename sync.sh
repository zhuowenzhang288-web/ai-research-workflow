#!/usr/bin/env bash
# sync.sh — 让 SKILL.md 和 scripts 从本仓（唯一源）同步到其他位置。
#
# 为什么需要：这份方法论存在三处副本，手工同步漏过好几次（图里的行数、脚本数量都错过）。
#   1. 本仓（源）            ai-research-workflow-repo/SKILL.md + scripts/
#   2. DSH bundle            dsh-research-agent/assets/ai-research-workflow/
#   3. DSH 本地技能目录      ~/.dsh/skills/ai-research-workflow/
#
# 用法:
#   ./sync.sh            # 同步 2 和 3
#   ./sync.sh --check    # 只检查是否一致，不改文件（可放 CI）
#   ./sync.sh --only 2   # 只同步 bundle
set -euo pipefail
cd "$(dirname "$0")"

SRC_SKILL="SKILL.md"
SRC_SCRIPTS="scripts"
# 本地目录名与 GitHub 仓名不一致（仓是 dsh-research-agent，目录是 dsh-ai-research-workflow），
# 所以两种都试，取存在的那个。
for cand in "../dsh-research-agent" "../dsh-ai-research-workflow"; do
  [[ -d "$cand/assets/ai-research-workflow" ]] && { BUNDLE_DIR="$cand/assets/ai-research-workflow"; break; }
done
BUNDLE_DIR="${BUNDLE_DIR:-../dsh-ai-research-workflow/assets/ai-research-workflow}"
DSH_DIR="$HOME/.dsh/skills/ai-research-workflow"

CHECK=0
ONLY=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --check) CHECK=1; shift;;
    --only) ONLY="$2"; shift 2;;
    -h|--help) sed -n '2,16p' "$0"; exit 0;;
    *) echo "未知参数: $1" >&2; exit 1;;
  esac
done

sha() { shasum -a 256 "$1" 2>/dev/null | awk '{print $1}'; }
diff_count=0
report() {  # report <标签> <目标目录>
  local label="$1" dst="$2"
  if [[ ! -d "$dst" ]]; then
    echo "  ⏭  $label: 目标不存在（$dst），跳过"
    return
  fi
  local bad=0
  [[ -f "$dst/SKILL.md" ]] && [[ "$(sha "$SRC_SKILL")" != "$(sha "$dst/SKILL.md")" ]] && { echo "  ❌ $label/SKILL.md 不一致"; bad=1; }
  for f in "$SRC_SCRIPTS"/*.py; do
    local n; n=$(basename "$f")
    [[ -f "$dst/scripts/$n" ]] || { echo "  ❌ $label/scripts/$n 缺失"; bad=1; continue; }
    [[ "$(sha "$f")" != "$(sha "$dst/scripts/$n")" ]] && { echo "  ❌ $label/scripts/$n 不一致"; bad=1; }
  done
  if [[ $bad -eq 0 ]]; then echo "  ✅ $label 已一致"; else diff_count=$((diff_count+1)); fi
}

copy_to() {  # copy_to <标签> <目标目录>
  local label="$1" dst="$2"
  [[ -d "$dst" ]] || { echo "  ⏭  $label: 目标不存在，跳过"; return; }
  mkdir -p "$dst/scripts"
  cp "$SRC_SKILL" "$dst/SKILL.md"
  cp "$SRC_SCRIPTS"/*.py "$dst/scripts/"
  echo "  ✅ $label 已同步"
}

echo "源: $(pwd)/$SRC_SKILL + $SRC_SCRIPTS/"
echo

if [[ $CHECK -eq 1 ]]; then
  echo "检查模式（不改文件）："
  [[ "$ONLY" == "" || "$ONLY" == "2" ]] && report "bundle" "$BUNDLE_DIR"
  [[ "$ONLY" == "" || "$ONLY" == "3" ]] && report "DSH 本地" "$DSH_DIR"
  echo
  if [[ $diff_count -gt 0 ]]; then
    echo "有 $diff_count 处不一致 → 运行 ./sync.sh 修复"
    exit 1
  fi
  echo "全部一致 ✓"
  exit 0
fi

echo "同步："
[[ "$ONLY" == "" || "$ONLY" == "2" ]] && copy_to "bundle" "$BUNDLE_DIR"
[[ "$ONLY" == "" || "$ONLY" == "3" ]] && copy_to "DSH 本地" "$DSH_DIR"
echo
echo "提示：bundle 装的是本地目录链接时，DSH 需重开会话或重载插件才读新内容。"
