# 9_7 — Multi-Agent with Claude Code (Vibe Coding)

## `multi-agent-claude-code-prompt.txt`

**What it does:**
This folder contains a prompt (not runnable code) used to generate a full multi-tool
AI agent project via Claude Code or another AI coding assistant.
The prompt describes requirements for a project called "Multi-Tool AI Agent" and lets
the AI write the entire codebase from the description.

**Tools described in the prompt:**
- Weather tool — Open-Meteo API (free, no key)
- Stock tool — yfinance
- Calculator tool — safe expression evaluator
- Web search — OpenAI built-in `web_search_preview`

**Things to learn:**
- What "vibe coding" means: describing what you want in plain language and letting AI generate the code
- How to write a good AI coding prompt: specify language, structure, tools, examples, and architecture
- The agent architecture described: user → agent → tool selection → response
- Real tool calling: the agent uses OpenAI function calling to decide which tool to invoke
- This is the capstone concept — combining tools + tool selection + natural language interface

**Key difference from previous sections:**
Previous sections hardcoded which function to call. This project uses real OpenAI function
calling — the LLM reads the user's message and decides which tool to invoke automatically.

---

**这个文件做什么：**
这个文件夹包含一个提示词（不是可运行的代码），用于通过 Claude Code 或其他 AI 编程助手
生成一个完整的多工具 AI agent 项目。
提示词描述了"Multi-Tool AI Agent"项目的需求，让 AI 根据描述编写整个代码库。

**提示词中描述的工具：**
- 天气工具——Open-Meteo API（免费，无需 key）
- 股票工具——yfinance
- 计算器工具——安全的表达式求值器
- 网络搜索——OpenAI 内置 `web_search_preview`

**可以学到什么：**
- 什么是"vibe coding"：用自然语言描述需求，让 AI 生成代码
- 如何写好 AI 编程提示词：指定语言、结构、工具、示例和架构
- 提示词中描述的 agent 架构：用户 → agent → 工具选择 → 响应
- 真正的 tool calling：agent 使用 OpenAI function calling 自动决定调用哪个工具
- 这是核心概念的综合——工具 + 工具选择 + 自然语言界面

**与前几节的关键区别：**
前几节硬编码了调用哪个函数。这个项目使用真正的 OpenAI function calling——
LLM 读取用户消息后自动决定调用哪个工具。
