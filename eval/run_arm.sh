#!/bin/bash
# 运行一臂一道题
#   ./run_arm.sh <noskill|skill> <任务名，如 Q1>
#
# 前置：
#   1. 已安装 opencode（https://opencode.ai）
#   2. 环境变量：AGENT_API_KEY（模型网关 key）
#   3. 每个臂目录下有 opencode.json 指向你的模型
set -euo pipefail
cd "$(dirname "$0")"
ARM="${1:?用法: run_arm.sh <noskill|skill> <任务名>}"
TASK="${2:?用法: run_arm.sh <noskill|skill> <任务名>}"

: "${AGENT_API_KEY:?请设置 AGENT_API_KEY}"

mkdir -p "arm-$ARM/$TASK"
cd "arm-$ARM/$TASK"

# 每个运行用独立数据目录，避免并发写同一个 sqlite 导致 "database is locked"
export XDG_DATA_HOME="${XDG_DATA_HOME:-$HOME/.local/share}/opencode-$ARM-$TASK"
mkdir -p "$XDG_DATA_HOME"

# 15 分钟硬超时（不含启动）
perl -e 'alarm 900; exec @ARGV' opencode run --auto "$(cat "../../tasks/$TASK.md")" > run.log 2>&1
echo "exit=$?"
