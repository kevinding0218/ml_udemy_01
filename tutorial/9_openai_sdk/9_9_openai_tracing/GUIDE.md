# 9_9 — OpenAI Tracing

## `openai_tracing.py / .ipynb`

**What it does:**
Same agent code as 9_8 but with tracing **enabled** (no `set_tracing_disabled`).
When tracing is on, every agent run is automatically recorded in OpenAI's tracing dashboard
so you can inspect inputs, outputs, token usage, and latency for each step.

**Things to learn:**
- What tracing is: automatic logging of agent runs — inputs, outputs, timing, token counts
- Tracing is on by default in `openai-agents` — 9_8 disabled it, this file leaves it on
- Where to see traces: platform.openai.com → Traces dashboard
- Why tracing matters: debugging agents is hard without visibility into what the LLM received and returned
- Compare with MLflow (section 3): both are observability tools, but tracing is for LLM calls specifically

**Tracing vs no tracing:**

| | 9_8 (tracing off) | 9_9 (tracing on) |
|---|---|---|
| `set_tracing_disabled(True)` | Yes | Not called |
| Runs logged to OpenAI? | No | Yes |
| Can debug in dashboard? | No | Yes |
| Costs anything extra? | — | No (free feature) |

**In production:** always leave tracing on — it's the first thing you check when an agent returns a wrong answer.

---

**这个文件做什么：**
与 9_8 的 agent 代码相同，但启用了追踪（没有 `set_tracing_disabled`）。
追踪开启后，每次 agent 运行都会自动记录到 OpenAI 的追踪面板，
可以查看每个步骤的输入、输出、token 用量和延迟。

**可以学到什么：**
- 什么是追踪：自动记录 agent 运行——输入、输出、时序、token 数
- 追踪在 `openai-agents` 中默认开启——9_8 禁用了它，本文件保持开启
- 在哪里查看追踪：platform.openai.com → Traces 面板
- 为什么追踪很重要：没有可见性就很难调试 agent 的问题
- 与 MLflow（第 3 节）对比：两者都是可观测性工具，但追踪专门用于 LLM 调用

**追踪 vs 不追踪：**

| | 9_8（追踪关闭） | 9_9（追踪开启） |
|---|---|---|
| `set_tracing_disabled(True)` | 有 | 没有调用 |
| 运行记录到 OpenAI？ | 否 | 是 |
| 能在面板中调试？ | 否 | 是 |
| 额外费用？ | — | 没有（免费功能） |

**生产环境建议：** 始终保持追踪开启——当 agent 返回错误答案时，这是首先要查的地方。
