# 9_8 — OpenAI Agents SDK

## `openai_agents_sdk.py / .ipynb`

**What it does:**
Introduces the `openai-agents` SDK — a higher-level library on top of the raw OpenAI API.
Defines named agents with `Agent(name, instructions, model)` and runs them with `Runner.run()`.
Shows two agents: a History Tutor and a Science Tutor.

**Things to learn:**
- `openai-agents` is a separate package (`pip install openai-agents`) — not the same as `openai`
- `Agent` class replaces writing `client.responses.create()` manually — cleaner abstraction
- `Runner.run(agent, prompt)` handles the full agent loop for you
- `result.final_output` — how to get the text response
- `set_tracing_disabled(True)` — disables OpenAI's tracing dashboard (enabled by default in this SDK)
- `await` is required — Runner.run() is async; this only works inside Jupyter or an async context

**Comparison — raw API vs Agents SDK:**

| | Raw OpenAI API (9_1 to 9_6) | Agents SDK (this file) |
|---|---|---|
| Define agent | Write a Python function | `Agent(name=..., instructions=..., model=...)` |
| Run agent | `client.responses.create(...)` | `await Runner.run(agent, prompt)` |
| Get output | `response.output_text` | `result.final_output` |
| Multi-agent | Manual, you orchestrate | Built-in (handoffs, pipelines) |

---

**这个文件做什么：**
介绍 `openai-agents` SDK——基于原始 OpenAI API 的更高层级库。
用 `Agent(name, instructions, model)` 定义命名 agent，用 `Runner.run()` 运行它们。
展示了两个 agent：历史导师和科学导师。

**可以学到什么：**
- `openai-agents` 是一个独立包（`pip install openai-agents`），不同于 `openai`
- `Agent` 类替代了手动写 `client.responses.create()`——更简洁的抽象
- `Runner.run(agent, prompt)` 帮你处理完整的 agent 循环
- `result.final_output`——如何获取文本响应
- `set_tracing_disabled(True)`——禁用 OpenAI 追踪面板（该 SDK 默认开启追踪）
- 需要 `await`——Runner.run() 是异步的，只能在 Jupyter 或异步上下文中使用

**对比——原始 API vs Agents SDK：**

| | 原始 OpenAI API（9_1 到 9_6） | Agents SDK（本文件） |
|---|---|---|
| 定义 agent | 写一个 Python 函数 | `Agent(name=..., instructions=..., model=...)` |
| 运行 agent | `client.responses.create(...)` | `await Runner.run(agent, prompt)` |
| 获取输出 | `response.output_text` | `result.final_output` |
| 多 agent | 手动，自己编排 | 内置支持（handoff、pipeline） |
