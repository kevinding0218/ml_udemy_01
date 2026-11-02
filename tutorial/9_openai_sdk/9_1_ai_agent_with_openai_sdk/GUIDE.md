# 9_1 — AI Agent with OpenAI SDK

## `ai_agent_with_openai_sdk.py / .ipynb`

**What it does:**
First introduction to wrapping an LLM call in a reusable function (`ask_agent`).
Shows how `instructions` sets the agent's role, and demos switching persona
(AI instructor → stock analyst) with the same function.

**Things to learn:**
- What an "agent" means at its simplest: a function with a system prompt + LLM call
- `instructions` parameter — sets the system prompt / agent persona
- How changing `instructions` changes behaviour without changing the model
- This is the foundation — no tools, no memory yet

**Agent progression in this series:**
```
9_1  ← you are here: basic agent (instructions only)
9_2  → add data from external functions (manual)
9_3  → expose agent as an API
9_4  → give agent real tools (web search)
9_5  → give agent memory
```

---

**这个文件做什么：**
首次将 LLM 调用封装成可复用函数（`ask_agent`）。
展示如何用 `instructions` 设定 agent 角色，并演示切换角色（AI 讲师 → 股票分析师）。

**可以学到什么：**
- "agent"最简单的含义：一个包含系统提示和 LLM 调用的函数
- `instructions` 参数——设定系统提示 / agent 角色
- 如何通过更改 `instructions` 改变行为，而不需要换模型
- 这是基础——还没有工具和记忆

**本系列的 Agent 进化路径：**
```
9_1  ← 当前位置：基础 agent（仅有 instructions）
9_2  → 从外部函数获取数据（手动方式）
9_3  → 将 agent 暴露为 API
9_4  → 给 agent 真正的工具（网络搜索）
9_5  → 给 agent 添加记忆
```
