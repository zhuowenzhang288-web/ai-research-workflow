#!/bin/bash
# ai-research-workflow 一键安装
# 用法:
#   ./install.sh                # 自动检测本机所有已支持的 agent 平台并安装
#   ./install.sh --platform dsh # 只装到指定平台（claude|codex|cursor|dsh|agents|opencode）
#   ./install.sh --dry-run      # 只打印将要做什么，不执行
#
# 安装内容: SKILL.md + scripts/ → 各平台 skills 目录
# AGENTS.md 是项目级文件，请按需复制到你的科研项目的根目录（自动注入，不漏触发）。

set -euo pipefail
cd "$(dirname "$0")"

DRY_RUN=0
ONLY=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --platform) ONLY="$2"; shift 2;;
    --dry-run)  DRY_RUN=1; shift;;
    -h|--help)  grep '^#' "$0" | head -8; exit 0;;
    *) echo "未知参数: $1" >&2; exit 1;;
  esac
done

SKILL_DIR="ai-research-workflow"
installed=()
skipped=()

try_install() {
  local name="$1" dir="$2"
  if [[ -n "$ONLY" && "$ONLY" != "$name" ]]; then return; fi
  if [[ -d "$dir" ]]; then
    local target="$dir/$SKILL_DIR"
    if [[ $DRY_RUN -eq 1 ]]; then
      echo "[dry-run] $name: cp SKILL.md scripts/ → $target/"
      installed+=("$name")
    else
      mkdir -p "$target"
      cp SKILL.md "$target/"
      rm -rf "$target/scripts"
      cp -r scripts "$target/scripts"
      installed+=("$name ($target)")
    fi
  else
    skipped+=("$name（未检测到 $dir）")
  fi
}

try_install "claude" "$HOME/.claude/skills"
try_install "codex"  "$HOME/.codex/skills"
try_install "cursor" "$PWD/.cursor/skills"
try_install "dsh"    "$HOME/.dsh/skills"
try_install "agents" "$HOME/.agents/skills"

echo
if [[ ${#installed[@]} -gt 0 ]]; then
  echo "✅ 已安装到: ${installed[*]}"
else
  echo "⚠️ 没有检测到已支持平台的 skills 目录，未安装任何平台。"
  echo "   可先用 --platform 指定，或手动按 README 的「30 秒开始用」一节操作。"
fi
[[ ${#skipped[@]} -gt 0 ]] && echo "⏭  跳过: ${skipped[*]}"

cat <<'TIP'

💡 建议再加一层保险：把 AGENTS.md 复制到你的科研项目根目录——
   核心纪律每次请求自动注入，skill 按需加载补全细节（双保险，见 README）。
TIP
