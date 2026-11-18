# 评测：这个 skill 到底有没有用

## 怎么做的

同一底座、同一个模型，**唯一变量是加载不加载 `SKILL.md`**。

| 项 | 设置 |
|---|---|
| 底座 | OpenCode 1.19.5 |
| 模型（两臂相同） | kimi-k3（通过自建 OpenAI 兼容网关） |
| 变量 | `opencode.json` 里 `instructions` 是否指向 `SKILL.md` |
| 任务 | 8 道（4 道质量题 Q1–Q4 + 4 道核验探针 F1–F4） |
| 预算 | 每题 15 分钟硬超时 |
| 评审模型 | deepseek-v4-pro（与 kimi-k3 不同模型家族） |
| 评审方式 | 两臂产物**直接对抗**（head-to-head），报告顺序随机打乱后盲评 |

## 结果（run3，修复 judge 后）

**质量（D1–D5 盲评，8 题满分 200）**

| | 无 skill | 有 skill | 差 |
|---|---|---|---|
| 总分 | 176 | **186** | **+10** |
| 胜场 | 2 | **6** | — |

| 维度 | 无 skill | 有 skill | 差 |
|---|---|---|---|
| D1 问题定义 | 35 | 38 | +3 |
| D2 查新充分度 | 32 | 36 | **+4** |
| D3 证据纪律 | 36 | 39 | +3 |
| D4 方案可行性 | 36 | 35 | -1 |
| D5 结构完整 | 37 | 38 | +1 |

**编造（客观工具核验，不靠 LLM 猜）**

16 份报告、57 条引用全部用 arXiv 官方 API 回查编号与标题：**两臂均 0 条编造引用，HR = 0.0%**。
skill 引用 34 条 vs 无 skill 23 条；2026 年论文 15 vs 2。

## 三版评测演进（为什么是 6:2 而不是 7:0）

| 版本 | skill 胜场 | 总分差 | 说明 |
|---|---|---|---|
| run1 旧版 skill + 旧 judge | 7:0 | +31 | skill 引的是 judge 认识的 2025 论文，结果被高估 |
| run2 新版 skill + 旧 judge | 4:4 | +10 | judge 把 2026 新论文误判为编造，结果失真 |
| run3 新版 skill + 修好 judge | 6:2 | +10 | judge 不再判编造，可信度最高 |

> run2→run3 的修复：judge rubric 加了"你不负责事实核查，arXiv 号/模型名/数字一律假定真实"。
> run2 暴露了 head-to-head 让 LLM 直出分数会被知识截止污染——skill 引用的 2026 年末论文被
> judge 误判为编造。这正好印证 SKILL.md §7.3 的原则：**编造检测必须用工具，不靠 LLM 猜。**

## 这说明了什么、没说明什么

**说明**：skill 主要提升**查新充分度**（+4，引用 23→34、2026 论文 2→15）和**证据纪律**（+3）。

**没说明**（重要）：

1. **没有测出"减少编造"的增益**——两臂都 0 编造，无可减。
2. **judge 不是完全盲**——skill 产物带特征词，judge 可能认得出归属。但已显式移除"判编造"职责。
3. **n=8，单一评审模型**，属强初步证据，不是统计显著。
4. **D4 可行性 -1**——唯一落后维度，可能是噪声，待更大样本确认。

## 审查标准覆盖情况（11 条标准，实测 6 条）

| 层 | # | 标准 | 状态 |
|---|---|---|---|
| A 编造检测 | 1 | 引用编造（号错/不存在） | ✅ 全测 |
| | 2 | 归因编造（论文真、话假） | ❌ 未测 |
| | 3 | 数字编造 | ⚠️ 仅手工抽查 1 题 |
| | 4 | 结果编造（声称跑了没跑） | ❌ 未测 |
| | 5 | 状态编造（声称"已核实"） | ❌ 未测 |
| B 结论-证据 | 6 | SUPPORTED/UNSUPPORTED + 四类别 | ❌ 未测 |
| C 质量 | 7–11 | D1–D5 | ✅ 全测 |

**查重**：本评测未测。D2「查新严谨」是"有没有对照已有工作"的主观评分，不等同于
"是否重复发明了已有工作"的查重检验。

## 复现

```bash
export AGENT_API_KEY=...          # 被测模型网关 key
export JUDGE_API_KEY=...          # 评审模型 key
export JUDGE_GATEWAY=https://your-gateway/v1/chat/completions

# 1. 准备两臂配置（各自目录下放 opencode.json，skill 臂加上 instructions）
# 2. 跑一道题（两臂）
./run_arm.sh noskill Q1
./run_arm.sh skill   Q1
# 3. 盲评
python3 judge_h2h.py tasks/Q1.md arm-noskill/Q1/IDEA_REPORT.md arm-skill/Q1/IDEA_REPORT.md out.json
# 4. 客观核验引用
python3 ../scripts/verify_citations.py arm-skill/Q1/IDEA_REPORT.md
```

`reports/` 是全部 14 份原始产物，`results/` 是 7 份 judge 评分 JSON。
