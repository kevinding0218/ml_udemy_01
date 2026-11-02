# 9_2 — Tool Calling AI Agent (Manual Approach)

## `tool_calling_ai_agent_with_openai_sdk.py / .ipynb`

**What it does:**
Introduces the concept of tools by manually calling `get_weather()` and passing the result
to the LLM. The LLM formats the weather data into a friendly response.

**Things to learn:**
- Why LLMs can't access real-time data on their own
- The manual tool pattern: YOU call the function, YOU paste the result into the prompt
- This is NOT real tool calling — the LLM never sees the function, never decides to call it
- Real tool calling (with `tools=` parameter) comes in section 9_4

**Manual vs real tool calling:**

| | This file (manual) | Real tool calling (9_4) |
|---|---|---|
| Who decides to call the function? | You (hardcoded) | The LLM |
| Who decides the argument (city)? | You | The LLM (extracted from user message) |
| What if user asks something else? | Always calls weather | LLM skips the tool or picks a different one |
| `tools=` in the API call? | No | Yes |

---

**这个文件做什么：**
通过手动调用 `get_weather()` 并将结果传给 LLM 来介绍工具的概念。
LLM 将天气数据格式化为友好的回复。

**可以学到什么：**
- 为什么 LLM 无法自行访问实时数据
- 手动工具模式：你调用函数，你将结果粘贴进提示词
- 这不是真正的 tool calling——LLM 看不到函数，也不决定是否调用
- 真正的 tool calling（使用 `tools=` 参数）在 9_4 中介绍

**手动方式 vs 真正的 tool calling：**

| | 本文件（手动） | 真正的 tool calling（9_4） |
|---|---|---|
| 谁决定调用函数？ | 你（硬编码） | LLM |
| 谁决定参数（城市名）？ | 你 | LLM（从用户消息中提取） |
| 用户问别的问题怎么办？ | 总是调用天气函数 | LLM 跳过工具或选择其他工具 |
| API 调用中有 `tools=` 吗？ | 没有 | 有 |
