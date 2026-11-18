# AI Research Workflow

一套**方向无关**的科研工作流 skill：把一个通用 agent 变成更守证据纪律的研究助手。

不是又一个"自动写论文"的框架，而是一份**操作纪律**——告诉 agent 什么时候该停下来查新、
怎么区分"论文事实 / 我方假设 / 实验结果"、什么时候不许把猜想说成结论、投稿前要过哪几道审计。

## 它解决什么问题

通用 agent 做科研任务时最常见的四个毛病：

1. **不查新就开干**——不知道这个想法是否已有人做过
2. **证据不分层**——把"我记得"和"论文里写的"混在一起写
3. **结论越界**——小规模实验的规律被说成普遍成立
4. **引用不经核验**——编号、作者、数字凭印象写

这个 skill 用可执行的规则和门控把这些堵住。

## 效果（有实测数据）

同一底座（OpenCode + kimi-k3）、同一批任务，**唯一变量是加载不加载这个 skill**，
由另一个模型家族（deepseek-v4-pro）盲评。8 题（4 质量 + 4 核验探针）：

| | 无 skill | 有 skill |
|---|---|---|
| 总分（满分 200） | 176 | **186**（+10） |
| 胜场 | 2 | **6** |

增益集中在：

- **查新充分度 +4**（满分 40）：引用数 23 → 34，2026 年最新论文 2 → 15
- **证据纪律 +3**：区分事实/假设/结果，诚实标注核验状态
- **问题定义 +3**：澄清真实任务、研究问题可检验

唯一落后：**方案可行性 -1**（集中在 2 题，可能是噪声，待更大样本确认）。

**客观防编造**（`verify_citations.py` 走 arXiv 官方 API）：16 份报告 **0 编造引用**。

完整评测协议、原始产物、评分 JSON 见 [`eval/`](eval/)。**评测的局限也写在里面**，请一并读。

> 一句话结论：它主要让产出**更严谨、查新更充分**，而不是"防止编造"——
> 后者在联网底座上没测出差异（两臂都 0 编造）。

## 特点

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
eval/                         # 评测：协议、任务、14 份产物、评分、局限
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

## 局限（请一并读）

- 评测 n=7、单一评审模型，属**强初步证据**，不是统计显著
- 防编造增益**未验证**：联网底座下两臂都 0 编造，没有可减的编造
- 审查标准 11 条中**只测了 6 条**（引用编造 + D1–D5），归因/结果/状态编造与结论-证据一致性未测
- **查重未测**：D2「查新严谨」是主观评分，不等于"是否重复发明已有工作"

## License

MIT
