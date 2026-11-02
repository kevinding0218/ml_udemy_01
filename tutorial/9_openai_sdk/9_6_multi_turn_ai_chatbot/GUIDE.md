# 9_6 — Multi-Turn AI Chatbot

## `multi_turn_ai_chatbot.py / .ipynb`

**What it does:**
Builds an interactive terminal chatbot using the OpenAI Responses API.
Maintains a `messages` list across turns so the agent remembers context.
The loop runs until the user types "exit".

**Things to learn:**
- Combines two concepts from earlier: agent function (9_1) + memory (9_5)
- `if question.lower() == "exit": break` — clean exit pattern for terminal loops
- `client.responses.create(input=messages)` — passing the full history as input
- The difference between this and section 8: uses the newer Responses API (`client.responses`) instead of the older Chat Completions API (`client.chat.completions`)

**Responses API vs Chat Completions API:**

| | Chat Completions (section 8) | Responses API (this file) |
|---|---|---|
| Endpoint | `client.chat.completions.create()` | `client.responses.create()` |
| System prompt | `{"role": "system", ...}` in messages | `instructions=` parameter |
| Output | `response.choices[0].message.content` | `response.output_text` |
| Newer? | Older, stable | Newer OpenAI SDK style |

---

**这个文件做什么：**
使用 OpenAI Responses API 构建一个交互式终端聊天机器人。
在多轮对话中维护 `messages` 列表，让 agent 记住上下文。
循环运行直到用户输入 "exit"。

**可以学到什么：**
- 结合了前两节的概念：agent 函数（9_1）+ 记忆（9_5）
- `if question.lower() == "exit": break`——终端循环的干净退出模式
- `client.responses.create(input=messages)`——将完整历史作为输入传入
- 与第 8 节的区别：使用更新的 Responses API，而非旧的 Chat Completions API

**Responses API vs Chat Completions API：**

| | Chat Completions（第 8 节） | Responses API（本文件） |
|---|---|---|
| 接口 | `client.chat.completions.create()` | `client.responses.create()` |
| 系统提示 | messages 中的 `{"role": "system", ...}` | `instructions=` 参数 |
| 输出 | `response.choices[0].message.content` | `response.output_text` |
| 新旧 | 较旧，稳定 | 较新的 OpenAI SDK 风格 |
