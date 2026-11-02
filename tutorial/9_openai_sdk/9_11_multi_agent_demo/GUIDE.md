# 9_11 — Multi-Agent Demo

## `multi_agent_demo.py / .ipynb`

**What it does:**
Coordinates three specialised agents in sequence to produce a professional stock alert email.
Each agent does one job: Price Analyst analyses the movement, News Researcher explains possible
reasons, and Investment Summary combines both into a polished email body.

**Things to learn:**
- What a multi-agent pipeline is: multiple agents, each with a focused role, passing results to the next
- Why specialised agents are better than one general agent: focused instructions = better output quality
- How to chain agents manually: run agent A, pass `result.final_output` as input to agent B
- The "pipeline" pattern vs the "single agent" pattern
- Combining real data (yfinance) + multi-agent analysis + email delivery (Resend)

**Agent pipeline:**
```
get_stock_info("MSFT")
        ↓
price_agent         → "The stock dropped 2.3%, which is significant because..."
        ↓
news_agent          → "Possible reasons include recent earnings miss and..."
        ↓
summary_agent       → combines both into a professional email
        ↓
send_email()        → delivered via Resend
```

**Key insight — why three agents instead of one:**
A single agent asked to "analyse price AND research news AND write an email" spreads attention
across three tasks. Three focused agents each excel at their one job and produce better
combined output — the same principle as microservices vs a monolith.

---

**这个文件做什么：**
协调三个专业 agent 按顺序工作，最终生成一封专业的股票提醒邮件。
每个 agent 只做一件事：价格分析师分析涨跌，新闻研究员解释可能的原因，
投资摘要 agent 将两者整合成精炼的邮件正文。

**可以学到什么：**
- 什么是多 agent 流水线：多个各司其职的 agent，将结果依次传递
- 为什么专业 agent 优于单一通用 agent：专注的指令 = 更好的输出质量
- 如何手动串联 agent：运行 agent A，将 `result.final_output` 作为输入传给 agent B
- "流水线"模式 vs "单一 agent"模式
- 组合真实数据（yfinance）+ 多 agent 分析 + 邮件发送（Resend）

**Agent 流水线：**
```
get_stock_info("MSFT")
        ↓
price_agent         → "股票下跌 2.3%，这很显著，因为..."
        ↓
news_agent          → "可能原因包括最近的财报不及预期..."
        ↓
summary_agent       → 将两者整合为专业邮件
        ↓
send_email()        → 通过 Resend 发送
```

**核心洞察——为什么要用三个 agent 而不是一个：**
让单个 agent 同时"分析价格 + 研究新闻 + 写邮件"会分散注意力。
三个专注的 agent 各自专精一项任务，组合输出质量更好——
这与微服务 vs 单体应用的原则相同。
