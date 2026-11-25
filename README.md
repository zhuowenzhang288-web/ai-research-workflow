# AI Research Workflow

一套**跨平台的科研工作流 skill**：不是"自动写论文"的框架，也不是纯文档，而是**操作纪律 + 可执行工具**的组合。

核心方法是**现象驱动**：不凭空想 idea，先在小系统里跑海量小实验找规律，由规律反推出 idea，再查新、再上卡验证。

## 为什么是"跨平台不锁死"

- `SKILL.md` 用的是通用 frontmatter 格式（`name` + `description`），Claude Code / Codex / Cursor / opencode / DSH 都认
- `scripts/` 里的脚本**只用 Python 标准库**，任何能跑 `bash` 的 agent 都能 `python3 xxx.py` 直接执行，不依赖任何框架的专属 API

## 能力（scripts/，都会真正干活）

| 脚本 | 环节 | 用法 |
|---|---|---|
| `novelty_check.py` | 查新 | `python3 scripts/novelty_check.py "关键词"` — 查 arXiv 出候选清单 |
| `experiment_log.py` | 实验日志 | `add` 记录一次 / `list` 汇总 keep·discard·crash |
| `verify_citations.py` | 引用核验 | 核验报告里的 arXiv/DOI，输出幻觉率 HR |
| `audit_chain.py` | 审计链 | 五层审计逐层判定，汇总 PASS/WARN/FAIL/BLOCKED |

> 四个脚本都是纯 Python 标准库，零第三方依赖。`python3 scripts/<名>.py --help` 看用法。

## 安装（各平台）

核心是同两份东西：`SKILL.md` + `scripts/`。放到各自的 skill 目录即可。

### Claude Code

```bash
mkdir -p ~/.claude/skills/ai-research-workflow
cp -r SKILL.md scripts ~/.claude/skills/ai-research-workflow/
```

### Codex

```bash
mkdir -p ~/.codex/skills/ai-research-workflow
cp -r SKILL.md scripts ~/.codex/skills/ai-research-workflow/
```

（或把 SKILL.md 内容并进项目的 `AGENTS.md`。）

### Cursor

```bash
mkdir -p .cursor/skills/ai-research-workflow
cp -r SKILL.md scripts .cursor/skills/ai-research-workflow/
```

### opencode

在项目的 `opencode.json` 里引用：

```json
{ "instructions": ["/path/to/ai-research-workflow/SKILL.md"] }
```

### DeepSeek Harness

```bash
mkdir -p ~/.dsh/skills/ai-research-workflow
cp -r SKILL.md scripts ~/.dsh/skills/ai-research-workflow/
```

也可以装 DSH 专属 bundle（一键安装），见 [dsh-ai-research-workflow](https://github.com/zhuowenzhang288-web/dsh-ai-research-workflow)。

> 各平台 skills 目录的准确路径以各平台最新文档为准；核心不变——`SKILL.md` 和 `scripts/` 过去就能用。

## 目录结构

```
SKILL.md                      # 工作流本体（现象驱动 + 查新 + 实验 + 审计）
scripts/
├── novelty_check.py          # 查新
├── experiment_log.py         # 实验日志
├── verify_citations.py       # 引用核验
└── audit_chain.py            # 五层审计
README.md
LICENSE
```

## 工作流概览

| 阶段 | 内容 |
|---|---|
| §0 触发 | 命中科研任务 → 告知 + 派子 agent（A/B/C 三档记忆隔离） |
| §1 选题 | **现象驱动优先**（先小实验找规律再想 idea）+ 反向追问 + 选题漏斗 + CCF-A 六维判断 |
| §2 查新 | `novelty_check.py` 拉候选 → 三轮核查 → 只读摘要不得 KEEP/KILL（取证标准）→ 撞车可深挖可证伪新预言 |
| §3 读论文 | 拆论文五要素 + 争议地图 |
| §4 实验 | 固定预算、基线先行、评测只读、`experiment_log.py` 记 keep/discard；§4.2.1 造现象发现循环 |
| §5 结论 | result-to-claim 三问 + claim 状态机 |
| §6 写作 | 先 story 后 paper + 写作契约 |
| §7 评审 | 模拟审稿 / 锚定评审 / `audit_chain.py` 五层审计链 |
| §8 回应 | Rebuttal 拆解 + 改投硬约束 |

## License

MIT