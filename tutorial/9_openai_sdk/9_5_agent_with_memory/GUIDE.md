# 9_5 — Agent with Memory

## `agent_with_memory.py / .ipynb`

**What it does:**
Adds conversation memory by maintaining a `messages` list across calls.
Each question and answer is appended, so the agent can answer follow-up questions
that refer to previous turns ("where does he teach?").

**Things to learn:**
- How to implement multi-turn memory: accumulate messages in a list, pass the full list each time
- The API is stateless — memory is an illusion you create by sending history each time
- The difference between this and section 8 (chatbot): same concept, applied inside an agent function
- Trade-off: longer history = better context, but more tokens = higher cost per call
- In production: history is usually stored in a database, not a Python list in memory

**Why "where does he teach?" works:**
```python
messages = [
    {"role": "user",      "content": "Who is Andrew Ng?"},
    {"role": "assistant", "content": "Andrew Ng is an AI pioneer..."},
    {"role": "user",      "content": "Where does he teach?"},   # ← "he" refers to prior context
]
# Full list sent → LLM sees the full conversation → can resolve "he"
```

---

**这个文件做什么：**
通过在调用之间维护一个 `messages` 列表来添加对话记忆。
每次的问题和回答都追加到列表中，agent 能回答引用之前内容的追问
（"他在哪里教书？"）。

**可以学到什么：**
- 如何实现多轮记忆：将消息累积到列表中，每次传入完整列表
- API 是无状态的——记忆是你通过每次发送历史来制造的"幻觉"
- 与第 8 节（聊天机器人）的区别：概念相同，用在 agent 函数内部
- 权衡：历史越长 = 上下文越好，但 token 越多 = 每次调用费用越高
- 生产环境中：历史通常存储在数据库中，而不是内存中的 Python 列表

**为什么"他在哪里教书？"能正确回答：**
```python
messages = [
    {"role": "user",      "content": "谁是 Andrew Ng？"},
    {"role": "assistant", "content": "Andrew Ng 是 AI 领域的先驱..."},
    {"role": "user",      "content": "他在哪里教书？"},   # ← "他"指的是上文的 Andrew Ng
]
# 完整列表发送 → LLM 看到完整对话 → 能解析"他"是谁
```
