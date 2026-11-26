<div align="center">

# 🕵️ 现象驱动 · AI 科研工作流

**先做实验找规律，再反推 idea。不凭空胡想。**

一套跨平台、带可执行工具的科研工作流 skill——把「AI agent 想 idea 很不靠谱」这个毛病，用**现象驱动**和**真能跑的脚本**治住。

[![License: MIT](https://img.shields.io/badge/License-MIT-FDE68A.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/zhuowenzhang288-web/ai-research-workflow?style=social)](https://github.com/zhuowenzhang288-web/ai-research-workflow/stargazers)
[![GitHub last commit](https://img.shields.io/github/last-commit/zhuowenzhang288-web/ai-research-workflow)](https://github.com/zhuowenzhang288-web/ai-research-workflow/commits)
[![GitHub repo size](https://img.shields.io/github/repo-size/zhuowenzhang288-web/ai-research-workflow)](https://github.com/zhuowenzhang288-web/ai-research-workflow)
[![Release](https://img.shields.io/badge/release-v1.0.0-DC2626.svg)](../../releases)

![架构图](docs/architecture.svg)

</div>

---

## 本仓是什么 · 两仓分工

**本仓 = 方法论本体（skill）**：跨平台的 `SKILL.md` + 6 个零依赖脚本。不绑任何 harness，Claude Code / Codex / Cursor / opencode / DSH 都能用。它回答"**科研该怎么做**"。

| 仓 | 角色 | 内容 |
|---|---|---|
| **ai-research-workflow**（本仓） | 跨平台方法/skill | SKILL.md + scripts + 评测证据 |
| **[dsh-research-agent](https://github.com/zhuowenzhang288-web/dsh-research-agent)** | DSH 深度集成 | 把本仓 skill 装进 DSH + 科研模式 preset + 人格 + 自动循环 |

想要"保证纪律在场、选模式即科研 agent"→ 用 DSH 版；想要"任何平台轻量即用"→ 用本仓。

---

## 你的 AI 是不是也这样？

| 痛点 | 表现 |
|---|---|
| 凭空胡想 idea | 张口就是几个听过八百遍的方向，查新一过就死 |
| 只读摘要就下结论 | 扫一眼 abstract 就说"这个没人做过"，其实正文里早写满了 |
| 题目越做越窄 | 方向死了就钻更窄的变体，每窄一级重付一轮查新+实验，token 哗哗烧 |
| 把猜想当结论 | "我认为""应该可以"，没有实验支撑，写成论文全露馅 |
| 引用凭印象编 | 编号、作者、数字随手写，一核准是错的 |

这些不是 AI 不够聪明，是**没有一套硬纪律 + 可执行工具**在压着它。

---

## 我们换了个思路：现象驱动

传统科研 workflow 是「先想 idea → 查新 → 做实验」。但 **agent 凭空想 idea 的能力很弱**——真实项目里连开 24 个方向，0 个存活。

**反过来**就通了——idea 是挖出来的，不是憋出来的：


在能精确测量的小系统里跑几百个秒级实验，让规律自己浮出来。下方色条标出 4 个配套脚本各自服务的环节。

---

## 不是又一份"提示词"，是能直接跑的脚本

纯文档谁都会写，这套带 **4 个零依赖脚本**（只靠 Python 标准库，任何 agent 跑 `bash` 就能用）：

| 脚本 | 干什么 | 一句话用法 |
|---|---|---|
| `novelty_check.py` | 查新 | `python3 scripts/novelty_check.py "GRPO collapse"` → 直接列出 arXiv 候选 |
| `novelty_report.py` | 查新取证校验 | 校验报告里每篇引用的「读取程度」标注，缺标即 FAIL |
| `funnel.py` | 选题漏斗 | `add` 记录 / `list` 过滤 / `narrow-watch` 防窄化预警 |
| `experiment_log.py` | 实验日志 | `add` 记一次 / `list` 汇总 keep·discard·crash |
| `verify_citations.py` | 引用核验 | 一键核验报告里的 arXiv/DOI，输出幻觉率 HR |
| `audit_chain.py` | 投稿审计 | 五层审计链；`verify-results` 自动查「结果编造」 |

---

## 双保险：AGENTS.md 兜底 + skill 补全

普通 skill 有个通病：**靠 agent 自觉加载，一忙就忘**——核心纪律再好，没加载等于没有。

这套工作流是两层设计：

| 层 | 内容 | 加载方式 |
|---|---|---|
| `AGENTS.md` | 33 行核心纪律（现象驱动 / 查新取证 / 证据四分 / 门控） | **每次请求自动注入**，不漏 |
| `SKILL.md` | 384 行完整方法论 + 6 条实战教训 | 按需加载，细节补全 |

用法：把 `AGENTS.md` 放到项目根目录（DSH 由 `dsh-agent-instructions` 插件自动注入；Claude Code / Codex 同理），再把 `SKILL.md` + `scripts/` 装进 skills 目录。核心纪律永远在场，完整方法论随取随用。

---

## 30 秒开始用

```bash
git clone https://github.com/zhuowenzhang288-web/ai-research-workflow
cd ai-research-workflow
./install.sh          # 自动检测本机 agent 平台，一键装好
```

`install.sh` 会自动找到你机器上已装的支持平台（Claude Code / Codex / Cursor / DSH / AGENTS）并拷贝 `SKILL.md` + `scripts/`。想手动或装到特定平台：

| 平台 | 命令 |
|---|---|
| **Claude Code** | `mkdir -p ~/.claude/skills/ai-research-workflow && cp -r SKILL.md scripts ~/.claude/skills/ai-research-workflow/` |
| **Codex** | `mkdir -p ~/.codex/skills/ai-research-workflow && cp -r SKILL.md scripts ~/.codex/skills/ai-research-workflow/` |
| **Cursor** | `mkdir -p .cursor/skills/ai-research-workflow && cp -r SKILL.md scripts .cursor/skills/ai-research-workflow/` |
| **opencode** | 在 `opencode.json` 里 `"instructions": ["/path/to/SKILL.md"]` |
| **DeepSeek Harness** | `mkdir -p ~/.dsh/skills/ai-research-workflow && cp -r SKILL.md scripts ~/.dsh/skills/ai-research-workflow/`（或装 [bundle](https://github.com/zhuowenzhang288-web/dsh-research-agent)） |

> 核心三份东西：`AGENTS.md`（放项目根目录，自动注入兜底）+ `SKILL.md` + `scripts/`（装进 skills 目录），放对位置就能用，不绑定任何框架。

---

## 它从真实项目里长出来，不是纸上谈兵

这套方法的每一个规则，都是在一个**单卡 ICML 选题项目**里用真金白银换来的：

- **检索型挖空位 24 方向 0 存活** → 才悟出"现象驱动"
- **一天内两个方向被"空白"骗了** → 才写下"找到空白≠值得补"
- **两个评测 bug 白烧 40+ 次 GPU** → 才定下"管道先验证"
- **一个方向连钻 5 个窄变体全死** → 才定下"窄 ≠ 安全：换方向 > 钻缝，深挖挖的是新维度不是收窄"

这些教训已整理成 6 条「实战教训」写进 SKILL.md，每条都标了现身章节。

---

## 目录

```
SKILL.md                  # 完整方法论（389 行 + 7 条实战教训）
AUTO_MODE.md              # 自动循环模式：skill + goal + schedule 拼法
scripts/
├── novelty_check.py      # 查新
├── novelty_report.py     # 查新取证校验
├── funnel.py             # 选题漏斗 + 防窄化预警
├── experiment_log.py     # 实验日志
├── verify_citations.py   # 引用核验
└── audit_chain.py        # 五层审计 + 结果编造检查
README.md
LICENSE
```

## License

MIT