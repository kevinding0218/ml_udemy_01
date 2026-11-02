# 9_3 — Deploy Agent with FastAPI

## `deploy_agent_with_fastapi.py / .ipynb`

**What it does:**
Wraps the LLM agent in a FastAPI endpoint (`POST /agent`) and exposes it publicly via ngrok.
Runs the server in a background thread so Colab doesn't block.

**Things to learn:**
- FastAPI basics: `@app.post`, `BaseModel` for request body validation, returning a dict as JSON
- `pydantic.BaseModel` — automatically parses and validates incoming JSON
- `uvicorn` — the ASGI server that runs FastAPI (equivalent to Flask's dev server)
- `ngrok` — tunnels your localhost to a public HTTPS URL (used for Colab demos)
- `nest_asyncio` — allows nested event loops needed when running uvicorn inside a Jupyter cell
- FastAPI vs Flask: FastAPI is async-first and auto-generates API docs at `/docs`

---

## `invoke_agent_fast_api.py / .ipynb`

**What it does:**
A simple client script that calls the deployed FastAPI endpoint via HTTP POST
using the public ngrok URL.

**Things to learn:**
- How to call any REST API from Python using `requests.post()`
- Separation of concerns: server (deploy) and client (invoke) are independent files
- The ngrok URL changes every session — you must update it each time you restart

---

**`deploy_agent_with_fastapi.py` 这个文件做什么：**
将 LLM agent 包装成 FastAPI 端点（`POST /agent`），并通过 ngrok 公开暴露。
在后台线程中运行服务器，以避免 Colab 阻塞。

**可以学到什么：**
- FastAPI 基础：`@app.post`、用 `BaseModel` 验证请求体、返回 dict 作为 JSON
- `pydantic.BaseModel`——自动解析和验证传入的 JSON
- `uvicorn`——运行 FastAPI 的 ASGI 服务器（相当于 Flask 的开发服务器）
- `ngrok`——将 localhost 隧道为公开 HTTPS URL（用于 Colab 演示）
- `nest_asyncio`——允许在 Jupyter cell 内部运行 uvicorn 所需的嵌套事件循环
- FastAPI vs Flask：FastAPI 默认异步，并在 `/docs` 自动生成 API 文档

---

**`invoke_agent_fast_api.py` 这个文件做什么：**
一个简单的客户端脚本，通过 ngrok 公开 URL 以 HTTP POST 方式调用已部署的 FastAPI 端点。

**可以学到什么：**
- 如何用 `requests.post()` 调用任意 REST API
- 关注点分离：服务端（deploy）和客户端（invoke）是独立文件
- ngrok URL 每次重启都会变——必须每次更新
