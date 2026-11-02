# Section 7 — OpenAI API Getting Started

## `openai_api_getting_started.py / .ipynb`

**What it does:**
First contact with the OpenAI API. Sends chat messages, gets JSON responses,
counts tokens, and generates an image with DALL-E 3.

**Things to learn:**
- How the `messages` array works: `system` sets the persona, `user` asks, `assistant` is prior replies
- Multi-turn conversation: pass the full history in each request so the model has context
- `response_format={"type": "json_object"}` — force structured JSON output
- `response.usage.total_tokens` — how to check token usage (affects cost)
- `client.images.generate()` — text-to-image via DALL-E 3

**Note:** The API key in the file is a placeholder — replace with your own from platform.openai.com.

---

**这个文件做什么：**
第一次接触 OpenAI API。发送聊天消息、获取 JSON 格式响应、
统计 token 数量，并用 DALL-E 3 生成图像。

**可以学到什么：**
- `messages` 数组的工作方式：`system` 设定角色，`user` 提问，`assistant` 是之前的回复
- 多轮对话：每次请求都传入完整历史，模型才有上下文
- `response_format={"type": "json_object"}`——强制输出结构化 JSON
- `response.usage.total_tokens`——如何查看 token 用量（影响费用）
- `client.images.generate()`——通过 DALL-E 3 实现文字生成图像

**注意：** 文件中的 API key 是占位符——请替换为你自己在 platform.openai.com 上的 key。
