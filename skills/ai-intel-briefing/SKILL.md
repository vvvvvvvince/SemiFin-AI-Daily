---
name: ai-intel-briefing
description: 每日 AI/Agent/产品/开源总览简报（总编日报 Skill）。
---

# ai-intel-briefing 每日总编简报

## 概述
本技能由 Agent 驱动，自动调度 RSS 收集和渲染逻辑，读取聚合后的原始 JSON，并利用大模型对其进行二次提炼与分级过滤，最终生成排版优雅的日报，写入用户的 Obsidian 库中。

## 工作流

### 第一步：收集数据（Python 管线）
1. 在项目根目录 `C:\Users\lidongye\.gemini\antigravity\scratch\ai-intel` 下运行：
   `python scripts/collect_rss.py; python scripts/collect_arxiv.py; python scripts/collect_github.py; python scripts/collect_xueqiu.py; python scripts/render_report.py`
   （如 Docker Desktop 已运行，也可用 `docker compose up --build` 替代）
2. 等待脚本执行完毕，确认 `reports/daily/{YYYY-MM-DD}_draft.md` 已生成。

### 第二步：实时拉取 Twitter 动态并合成简报
**重要：必须先读 `reports/daily/{YYYY-MM-DD}_draft.md` 获取骨架数据（包含 RSS、ArXiv、GitHub 以及已配置 Cookie 的雪球行情和热帖数据），以防止原始 JSON 截断问题。**

1. 用 `view_file` 读取 `reports/daily/{YYYY-MM-DD}_draft.md`。
2. 执行以下命令，实时拉取 @aleabitoreddit（白毛股神）最新 10 条推文（系统已自动读取环境变量中的 TWITTER_AUTH_TOKEN 和 TWITTER_CT0）：
   `& "$env:USERPROFILE\.agent-reach-venv\Scripts\twitter.exe" search --from aleabitoreddit -t latest -n 10 --full-text`
3. 将 draft.md 中的全部板块（含雪球）、Twitter 实时推文进行汇总，结合用户关注重点（Agent/MCP/OCR/私有化/半导体/BTC/RWA），使用以下结构进行精炼：

```markdown
---
title: {YYYY-MM-DD} AI Daily Briefing
project: AI 行业观察
type: 研究笔记
tags: [ai-daily, tech-trends, mcp, ocr]
date: {YYYY-MM-DD}
source: Antigravity总编
status: 📝草稿
---

# AI Daily — {YYYY-MM-DD}

## 必看 3 条
- **标题**
  - **发生了什么**：{简述}
  - **为什么重要**：{分析}
  - **对我的项目有什么影响**：{与开发、医药等项目关联的实际价值}

## 可试验 2 条
- **新模型 / 新工具 / 新开源项目**
  - **推荐验证动作**：30 分钟内如何跑通测试 PoC。

## 项目相关
- **Agent / MCP / PDF / OCR / 私有化部署 / 医药 AI** 分类热点分析。

## AI x Crypto 交叉追踪
- **去中心化物理基础设施(DePIN)与代币化资产(RWA)**：汇总加密市场的 AI 相关基建、算力调度以及代币化股票等 RWA 在合规与发行动力方面的动态。

## 交易市场风险预警 (🚨 核心关注)
- 从财经、半导体供应链、宏观流动性和 Crypto 视角出发，提取可能导致波动和暴雷的风险信号：例如上游材料/光互连产能受限（参考白毛股神等博主）、美联储流动性缩紧、重要 AI 硬件出货延迟等可能危及现货市场（BTC/股票）的信号。

## GitHub 热门趋势 (Trending Top 10)
- 必须将底层 draft.md 中提取到的 GitHub Trending 前 10 名完整保留，列出排名、仓库名、一句话简介，并附带正确的 markdown 链接。

## 需要跟踪
- 未来 7 天内可能值得注意的 Release 预告、事件或发布会。

## 今日忽略
- {简述今天过滤掉的噪音，如营销稿、无 Demo 套壳、大额融资新闻}
```

### 第三步：写入 Obsidian
1. 检查是否存在路径：`C:\Users\lidongye\Desktop\Obsidian Vault\Projects\AI 行业观察\研究笔记\`。
2. 将上述 Markdown 内容保存为：`C:\Users\lidongye\Desktop\Obsidian Vault\Projects\AI 行业观察\研究笔记\{YYYY-MM-DD}_AI_Daily.md`。
3. 保存成功后，向用户汇报日报的主要看点。
