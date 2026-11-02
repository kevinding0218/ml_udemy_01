# Section 8 — ChatGPT OpenAI Chatbot

## `chatgpt_openai_chatbot.py / .ipynb`

**What it does:**
Builds an interactive terminal chatbot that maintains conversation history across turns.
The user types, the assistant replies, and the full history grows with each exchange.

**Things to learn:**
- How memory works in LLM chat: the API is stateless — you must send the full history every time
- The `messages` list as the conversation state — grows each turn
- Why the model can answer follow-up questions ("where was it played?") — prior context is in the list
- `while True` loop pattern for interactive terminal apps

**Key concept — why LLMs appear to "remember":**
The API has no memory between calls. What looks like memory is you resending
the entire conversation history on every request. Remove old messages and the model forgets.

---

**这个文件做什么：**
构建一个交互式终端聊天机器人，在多轮对话中保持对话历史。
用户输入，助手回复，每次交流后历史记录不断增长。

**可以学到什么：**
- LLM 聊天中"记忆"的工作原理：API 是无状态的——每次必须发送完整历史
- `messages` 列表作为对话状态——每轮都会增长
- 为什么模型能回答追问——因为之前的上下文已经在列表里了
- 交互式终端应用的 `while True` 循环模式

**核心概念——为什么 LLM 看起来能"记住"内容：**
API 在调用之间没有记忆。看似有记忆，是因为你每次请求都重新发送了完整的对话历史。
如果删掉旧消息，模型就会"忘记"。
