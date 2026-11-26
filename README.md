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
| **DeepSeek Harness** | `mkdir -p ~/.dsh/skills/ai-research-workflow && cp -r SKILL.md scripts ~/.dsh/skills/ai-research-workflow/`（或装 [bundle](https://github.com/zhuowenzhang288-web/dsh-ai-research-workflow)） |

> 核心三份东西：`AGENTS.md`（放项目根目录，自动注入兜底）+ `SKILL.md` + `scripts/`（装进 skills 目录），放对位置就能用，不绑定任何框架。

---

## 真实 A/B：同一个任务，裸 agent vs 加载 skill

不是嘴上说有用——同一底座（OpenCode + kimi-k3）、同一道题（「经验记忆的自动修订」选题报告），唯一变量是加不加载本 skill，由另一个模型家族盲评：

| | 无 skill（裸 agent） | 有 skill |
|---|---|---|
| 引用 | 只提论文名，无编号、无核验 | 每篇带 arXiv 号，开头注明"检索 8 组关键词逐条核实" |
| 证据纪律 | 假设与事实混写 | 显式标「我方推测」，还设了反向假设 H3 |
| 差异论证 | 一段并列描述 | 与 4 篇最接近工作逐条 1v1 对应 |
| 风险意识 | 无 | 写明"H1 可能不成立，届时降级为人工确认" |
| **盲评总分** | **18/25** | **24/25** |

<details>
<summary><b>▶ 无 skill 版（节选）</b>——写得顺，但全程无核验痕迹</summary>

> 真实场景：Voyager 式技能库、Reflexion 式教训记忆、A-MEM/MemGPT 式长期条目……代表性工作：(1) Reflexion（NeurIPS'23）与 Voyager（ICML'24）：纯追加式……(3) A-MEM（NeurIPS'25）：新条目触发旧条目属性更新……
>
> 待验假设 H1：跨条目矛盾数对失败轨迹的区分度优于条目年龄；H2：软修订的有用条目保留率显著高于硬删除……

论文名随手写，没有编号——其中 A-MEM 标成 NeurIPS'25，**这个归属根本没核过**。
</details>

<details>
<summary><b>▶ 有 skill 版（节选）</b>——每个事实都能指回来源</summary>

> （查新：arXiv 检索 8 组关键词并逐条核实；机制为摘要级论文事实，差异与空白为我方判断。）
>
> - **MemoryBank**（arXiv:2305.10250）：艾宾浩斯曲线时间衰减……
> - **PACMI**（arXiv:2610.05732, 2026-10）：溯源图 + 四态有效性格……
>
> 待验假设（我方推测）：H1……H3（反向）：THEANINE（arXiv:2406.10996）主张保留过时记忆——修订可能损害需历史上下文的任务。
>
> 风险：成败信号噪声大（H1 可能不成立），届时降级为"发现+人工确认修订"。

</details>

8 道题的完整评测中，本题两臂产物与盲评原文已存档在 [docs/before-after/](docs/before-after/)——可自行复核每一个字。

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