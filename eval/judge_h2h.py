#!/usr/bin/env python3
"""judge_h2h — 两臂直接对抗评审（head-to-head）。

用法:
    export JUDGE_API_KEY=sk-...
    export JUDGE_GATEWAY=https://your-gateway.example.com/v1/chat/completions
    python3 judge_h2h.py <task.md> <报告A.md> <报告B.md> <out.json>

两份报告顺序随机打乱后交给评审模型盲评，输出各自 D1-D5 分数与谁更好。
out.json 里的 report1/report2 字段用于还原真实臂属。
"""
import sys
import os
import json
import ssl
import time
import random
import urllib.request

GATEWAY = os.environ.get("JUDGE_GATEWAY", "")
MODEL = os.environ.get("JUDGE_MODEL", "deepseek-v4-pro")

RUBRIC = """你是严格、挑剔的科研评审。下面同一任务的两位 agent 各写了一份报告（标注为"报告X"和"报告Y"，顺序已随机打乱，与水平无关）。
请对每份报告在 5 个维度打分（各 1-5 分），并判断哪份整体更好。

【重要前提：你不负责事实核查】
报告里出现的任何 arXiv 编号（包括 2026 年甚至更晚的月份）、任何模型名（如 GPT-6-Astra、任何你没听过的名字）、任何具体数字，都一律假定为真实、已由独立核验工具确认。
不要因为"这个编号看起来太新"、"这个模型我不认识"、"这个数字存疑"而扣分——那不在你的职责内，而且会引入知识截止偏差。
你只评估报告作为一份科研产物的论证质量本身。

维度：
- D1 问题定义：是否澄清真实任务，研究问题是否具体可回答
- D2 查新充分度：是否对照了已有工作、对照是否具体（有编号/来源），是否说明检索范围与局限
- D3 证据纪律：是否区分事实/假设/推测，是否诚实标注了核验状态与不确定处，有无把猜想写成结论
- D4 方案可行性：假设是否可检验，最小实验是否具体可执行
- D5 结构完整：要素是否齐全、逻辑是否闭环

只输出 JSON，不要任何其他文字：
{
  "X": {"D1": 1, "D2": 1, "D3": 1, "D4": 1, "D5": 1},
  "Y": {"D1": 1, "D2": 1, "D3": 1, "D4": 1, "D5": 1},
  "better": "X|Y|tie",
  "rationale": "200字内，指出各自最强点和最弱点"
}"""


def judge_once(task, rep_x, rep_y):
    key = os.environ.get("JUDGE_API_KEY")
    if not key:
        raise RuntimeError("请设置 JUDGE_API_KEY")
    if not GATEWAY:
        raise RuntimeError("请设置 JUDGE_GATEWAY")

    prompt = f"{RUBRIC}\n\n【任务】\n{task}\n\n【报告X】\n{rep_x}\n\n【报告Y】\n{rep_y}"
    body = json.dumps({
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "你是严格的科研评审。只输出符合 schema 的 JSON。"},
            {"role": "user", "content": prompt},
        ],
        "response_format": {"type": "json_object"},
    }).encode()

    ctx = ssl.create_default_context()
    if os.environ.get("JUDGE_INSECURE_TLS") == "1":
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

    for attempt in range(4):
        try:
            req = urllib.request.Request(GATEWAY, data=body, headers={
                "Authorization": f"Bearer {key}",
                "Content-Type": "application/json",
            })
            with urllib.request.urlopen(req, context=ctx, timeout=300) as r:
                resp = json.load(r)
            verdict = json.loads(resp["choices"][0]["message"]["content"])
            verdict["_model"] = resp.get("model")
            verdict["_usage"] = resp.get("usage")
            return verdict
        except Exception as e:
            print(f"  [retry {attempt + 1}] {str(e)[:80]}", file=sys.stderr)
            time.sleep(8)
    return None


def main():
    if len(sys.argv) != 5:
        print(__doc__)
        sys.exit(1)
    task_f, rep1_f, rep2_f, out_f = sys.argv[1:5]
    task = open(task_f, encoding="utf-8").read()
    rep1 = open(rep1_f, encoding="utf-8").read()
    rep2 = open(rep2_f, encoding="utf-8").read()

    order = [rep1, rep2]
    random.shuffle(order)
    rep1_first = order[0] == rep1

    verdict = judge_once(task, order[0], order[1])
    if verdict is None:
        print(f"FAIL: 无法完成评审 {rep1_f} vs {rep2_f}", file=sys.stderr)
        sys.exit(1)

    if rep1_first:
        real = {"rep1": verdict.get("X", {}), "rep2": verdict.get("Y", {})}
        better = {"X": "rep1", "Y": "rep2", "tie": "tie"}.get(verdict.get("better", "tie"), "tie")
    else:
        real = {"rep1": verdict.get("Y", {}), "rep2": verdict.get("X", {})}
        better = {"X": "rep2", "Y": "rep1", "tie": "tie"}.get(verdict.get("better", "tie"), "tie")

    out = {
        "task": task_f,
        "report1": rep1_f,
        "report2": rep2_f,
        "scores": {"rep1": real["rep1"], "rep2": real["rep2"]},
        "better": better,
        "rationale": verdict.get("rationale", ""),
        "_model": verdict.get("_model"),
        "_usage": verdict.get("_usage"),
    }
    with open(out_f, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"saved: {out_f}  (better={better})")


if __name__ == "__main__":
    main()
