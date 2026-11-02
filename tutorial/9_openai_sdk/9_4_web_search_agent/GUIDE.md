# 9_4 — Web Search Agent

## `web_search_agent.py / .ipynb`

**What it does:**
Gives the LLM real-time web search capability by passing `tools=[{"type": "web_search_preview"}]`.
The LLM decides on its own when to search and what to search for.

**Things to learn:**
- This is the first real `tools=` usage — the LLM drives the decision, not your code
- `web_search_preview` is a built-in hosted tool — no function for you to write or execute
- The LLM automatically searches when the question requires current information
- Contrast with 9_2: there YOU called the function; here the LLM calls the tool itself
- Built-in (server-side) tools vs custom (user-defined) tools — both use `tools=` but work differently

**Real tool calling flow here:**
```
User: "What are today's top AI news?"
         ↓
LLM sees tools=[web_search_preview]
LLM decides: I need to search
         ↓
OpenAI servers execute the search (not your code)
         ↓
LLM gets results → generates summarised response
```

---

**这个文件做什么：**
通过传入 `tools=[{"type": "web_search_preview"}]` 给 LLM 赋予实时网络搜索能力。
LLM 自行决定何时搜索以及搜索什么。

**可以学到什么：**
- 这是第一次真正使用 `tools=`——由 LLM 驱动决策，而不是你的代码
- `web_search_preview` 是内置的托管工具——你不需要编写或执行任何函数
- 当问题需要最新信息时，LLM 会自动搜索
- 与 9_2 的对比：9_2 中你调用函数；这里 LLM 自己调用工具
- 内置（服务端）工具 vs 自定义（用户定义）工具——都用 `tools=`，但工作方式不同

**这里的真正 tool calling 流程：**
```
用户："今天 AI 领域的头条新闻是什么？"
         ↓
LLM 看到 tools=[web_search_preview]
LLM 决定：我需要搜索
         ↓
OpenAI 服务器执行搜索（不是你的代码）
         ↓
LLM 获得结果 → 生成摘要回复
```
