# AI Research Workflow

一套**方向无关**的科研工作流 skill：把一个通用 agent 变成更守证据纪律的研究助手。

核心方法是**现象驱动**：不凭空想 idea，先在小系统里跑海量小实验找规律，由规律反推出 idea，
再查新、再上卡验证。其余是一套操作纪律——什么时候该停下来查新、
怎么区分"论文事实 / 我方假设 / 实验结果"、什么时候不许把猜想说成结论、投稿前要过哪几道审计。

## 它解决什么问题

通用 agent 做科研任务时最常见的五个毛病：

1. **凭空想 idea**——不从小实验找规律，凭直觉想 idea，存活率低、大概率白做
2. **不查新就开干**——不知道这个想法是否已有人做过
3. **证据不分层**——把"我记得"和"论文里写的"混在一起写
4. **结论越界**——小规模实验的规律被说成普遍成立
5. **引用不经核验**——编号、作者、数字凭印象写

这个 skill 用可执行的规则和门控把这些堵住。

## 特点

- **现象驱动**：不凭空想 idea，先小实验找规律、由规律反推 idea（§4.2.1 造现象发现循环）
- **不绑定模型与框架**：纯 Markdown，任何能读 instructions 的 agent 都能用
- **模块化**：按阶段取用，不强制走完全链路；文末有路由速查表
- **门控明确**：查新通过、扩大实验、投稿出稿三处必须停下等人
- **带工具**：`scripts/verify_citations.py` 客观核验引用（输出幻觉率 HR），不靠 LLM 猜

## 安装

### OpenCode

```json
// opencode.json
{
  "instructions": ["/path/to/SKILL.md"]
}
```

### Claude Code / Cursor / Codex

把 `SKILL.md` 放进项目的规则文件，或直接引用：

```bash
# Claude Code
mkdir -p ~/.claude/skills/ai-research-workflow
cp SKILL.md ~/.claude/skills/ai-research-workflow/SKILL.md
```

Cursor / Codex 等：把 `SKILL.md` 内容追加到 `.cursorrules` / `AGENTS.md` / `CLAUDE.md`。

### DeepSeek Harness

```bash
mkdir -p ~/.dsh/skills/ai-research-workflow/scripts
cp SKILL.md ~/.dsh/skills/ai-research-workflow/
cp scripts/verify_citations.py ~/.dsh/skills/ai-research-workflow/scripts/
```

## 目录

```
SKILL.md                      # 工作流本体（9 节 + 路由速查）
scripts/verify_citations.py   # 引用核验工具：arXiv/DOI → 幻觉率 HR
```

## 工作流概览

| 阶段 | 内容 |
|---|---|
| §0 总原则 | 证据四分、单一事实源、执行/评审分离、门内自主门前停人 |
| §0 触发机制 | 命中即告知"正在查找"并派子 agent；子 agent 结构化汇报；记忆共享按耦合度分 A/B/C 三档（评审者与执行者永不共享） |
| §1 选题 | **现象驱动优先**（先小实验找规律再想 idea，不凭空想）→ 反向追问五问 + 选题漏斗（含失败想法） |
| §1.3 顶会适配 | CCF-A 六维打分 + 红旗项（加重审查、不一票否决），判断 idea 够不够 A 类 |
| §2 查新 | 三轮定向核查 + 非论文渠道 + "找到空白先问两句"，分级处理不一刀切 |
| §3 读论文 | 拆论文五要素 + 争议地图（共识/分歧/空白） |
| §4 实验 | §4.2.1 造现象发现循环（出 idea 的入口）+ 固定预算、基线先行、评测只读、keep/discard 日志 |
| §5 结论 | result-to-claim 三问 + claim 状态机（supported/invalidated/pending） |
| §6 写作 | 先 story 后 paper、写作契约、生成-评估-适配循环 |
| §7 评审 | 模拟挑剔审稿人 / 锚定评审 / 三层审计链 |
| §8 回应 | Rebuttal 拆解 + 改投硬约束 |
| §10 参考来源 | 方法论出处（Idea2Paper / autoresearch / ARIS / REASONS / intra-paper 等） |

## CCF-A 适配性判断（§1.3）

对已完成查新的 idea 做六维打分（问题重要性 / 新颖性 / 方法深度 / 证据强度 / 叙事潜力 / venue fit，各 1–5），
另设 5 类红旗项（有直接先例、增量调参、无可核验结果路径、单数据集、依赖不可复现环境）——触发加重审查，**不一票否决**。
总分 ≥24 且新颖性与问题重要性均 ≥4 → 强 A 候选；18–23 → 补强后重判；<18 → 不够 A；仅实质重复且差异不成立才淘汰。
这是研究判断，不是录用概率；venue fit 须对照目标 venue 近 3 年论文。

## 参考来源

本 skill 的方法论出处（详见 SKILL.md §10）：

| 来源 | 借鉴了什么 |
|---|---|
| [Idea2Paper / Idea2Story](https://github.com/AgentAlphaAGI/Idea2Paper) | 结构化 story 中间表示、锚定式盲评、检索辅助查新 |
| [karpathy/autoresearch](https://github.com/karpathy/autoresearch) | 固定预算实验循环、keep/discard 日志、简洁性准则 |
| [ARIS](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep) | 执行/评审分离、门控与多层审计、artifact 契约 |
| [REASONS](https://arxiv.org/abs/2405.02228) | 引用幻觉率 HR 客观指标 → `verify_citations.py` |
| [Intra-paper verification](https://github.com/Ranjitha2493/intra-paper-claim-verification) | 结论-证据一致性、SUPPORTED/UNSUPPORTED 判据 |

## 引用核验工具

```bash
python3 scripts/verify_citations.py 你的报告.md
```

输出：

```
总引用 12 | 核验通过 12 | 编造/不存在 0 | 无法核验 0
Hallucination Rate (HR) = 0.0%
```

仅依赖 Python 标准库。HR > 0 即说明报告里有查不到的引用。

## License

MIT
