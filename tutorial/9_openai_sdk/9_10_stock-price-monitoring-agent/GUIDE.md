# 9_10 — Stock Price Monitoring Agent

## `resend_email.py / .ipynb`

**What it does:**
A warmup file — sends a test HTML email via the Resend API.
Run this first to confirm your Resend API key works before building the full agent.

**Things to learn:**
- What Resend is: a developer email API (like SendGrid) — `pip install resend`
- How to send HTML email programmatically in Python
- Pattern: always test individual components (email) before wiring them into a larger system

---

## `stock_price_monitoring_agent.py / .ipynb`

**What it does:**
A complete automated agent that monitors a stock (Micron / MU), and if the price
moves more than 1%, uses an LLM to write a summary and emails it via Resend.
Runs on a 1-minute schedule indefinitely.

**Things to learn:**
- `yfinance` — free library to fetch real stock prices from Yahoo Finance
- Threshold logic: only trigger the agent when something meaningful happens (`abs(change) >= 1.0`)
- `schedule` library — runs a function on a repeating schedule (`every(1).minutes`)
- Combining real data (yfinance) + AI summarisation (Agent) + notification (Resend email)
- `async def check_stock()` + `asyncio.create_task()` — running async agent inside a sync scheduler
- `nest_asyncio.apply()` — needed to run async code inside Jupyter

**Architecture:**
```
Every 1 minute
    ↓
get_stock_info("MU")         ← yfinance (real data)
    ↓
if |change| >= 1%
    ↓
Runner.run(agent, prompt)    ← LLM writes the summary
    ↓
send_email(subject, body)    ← Resend delivers the email
```

---

**`resend_email.py` 这个文件做什么：**
热身文件——通过 Resend API 发送一封测试 HTML 邮件。
在构建完整 agent 之前先运行这个，确认你的 Resend API key 可用。

**可以学到什么：**
- Resend 是什么：面向开发者的邮件 API（类似 SendGrid）——`pip install resend`
- 如何用 Python 以编程方式发送 HTML 邮件
- 模式：在将组件（邮件）接入更大系统之前，先单独测试它

---

**`stock_price_monitoring_agent.py` 这个文件做什么：**
一个完整的自动化 agent，监控股票（美光科技 / MU），
如果价格变动超过 1%，使用 LLM 写摘要并通过 Resend 发送邮件。
无限循环，每分钟运行一次。

**可以学到什么：**
- `yfinance`——从 Yahoo Finance 免费获取真实股价的库
- 阈值逻辑：只在有意义的事件发生时触发 agent（`abs(change) >= 1.0`）
- `schedule` 库——按重复计划运行函数（`every(1).minutes`）
- 组合真实数据（yfinance）+ AI 摘要（Agent）+ 通知（Resend 邮件）
- `async def` + `asyncio.create_task()`——在同步调度器中运行异步 agent
- `nest_asyncio.apply()`——在 Jupyter 中运行异步代码的必要步骤

**架构：**
```
每 1 分钟
    ↓
get_stock_info("MU")         ← yfinance（真实数据）
    ↓
如果 |变动幅度| >= 1%
    ↓
Runner.run(agent, prompt)    ← LLM 写摘要
    ↓
send_email(subject, body)    ← Resend 发送邮件
```
