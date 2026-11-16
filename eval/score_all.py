#!/usr/bin/env python3
"""score_all — 汇总 8 题两臂的客观防编造 HR + 两臂对抗评分，出最终结论表。

用法: python3 score_all.py
前置: 各题 arm-noskill/<T>/IDEA_REPORT.md 与 arm-skill/<T>/IDEA_REPORT.md 已生成。
"""
import json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
TASKS = ["Q1", "Q2", "Q3", "Q4", "F1", "F2", "F3", "F4"]
VFY = os.path.join(os.path.dirname(HERE), "..", "..", "..", ".dsh/skills/ai-research-workflow/scripts/verify_citations.py")
# 绝对路径回退
if not os.path.exists(VFY):
    VFY = "/Users/omegahodge/.dsh/skills/ai-research-workflow/scripts/verify_citations.py"
JUDGE = os.path.join(HERE, "judge_h2h.py")

def run_vfy(report, out):
    r = subprocess.run([sys.executable, VFY, report, "--json", out],
                       capture_output=True, text=True, cwd=HERE)
    if not os.path.exists(out):
        return None
    return json.load(open(out))

def run_judge(task, r1, r2, out):
    r = subprocess.run([sys.executable, JUDGE, task, r1, r2, out],
                       capture_output=True, text=True, cwd=HERE)
    if not os.path.exists(out):
        return None
    return json.load(open(out))

def main():
    results = {}
    for t in TASKS:
        nf = os.path.join(HERE, f"arm-noskill/{t}/IDEA_REPORT.md")
        sf = os.path.join(HERE, f"arm-skill/{t}/IDEA_REPORT.md")
        if not (os.path.exists(nf) and os.path.exists(sf)):
            print(f"[跳过] {t}: 缺报告 (noskill={os.path.exists(nf)}, skill={os.path.exists(sf)})")
            continue
        # 客观防编造
        n_hr = run_vfy(nf, os.path.join(HERE, f"results/hr_noskill_{t}.json"))
        s_hr = run_vfy(sf, os.path.join(HERE, f"results/hr_skill_{t}.json"))
        # 两臂对抗
        j = run_judge(os.path.join(HERE, f"tasks/{t}.md"), nf, sf,
                      os.path.join(HERE, f"results/judge_{t}.json"))
        results[t] = {"hr_noskill": n_hr, "hr_skill": s_hr, "judge": j}
        print(f"[完成] {t}: HR noskill={n_hr['hallucination_rate'] if n_hr else '?'} "
              f"skill={s_hr['hallucination_rate'] if s_hr else '?'} "
              f"better={j['better'] if j else '?'}")

    json.dump({k: {kk: (vv if not isinstance(vv, dict) or True else vv) for kk, vv in v.items()}
               for k, v in results.items()}, open(os.path.join(HERE, "results/all.json"), "w"),
              ensure_ascii=False, indent=2, default=str)
    print("\n全部评分完成 → results/all.json")

if __name__ == "__main__":
    main()
