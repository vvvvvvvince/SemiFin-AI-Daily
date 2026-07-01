# 👁️ SemiFin AI Daily

一个部署在本地的 **AI 研发情报聚合与产业链投研提炼系统**。它采用轻量化的数据管道，自动捕获全网前沿技术动态，并结合大模型（LLM）进行过滤、分级，最终每天为你的 Obsidian 知识库输出一份高含金量的《AI Daily》简报。

---

## 🌟 核心能力

*   **📰 官方与个人博客 (RSS)**：追踪 OpenAI、DeepMind、Nvidia、Hugging Face 官方发布，以及 Simon Willison、Stratechery 等技术大牛个人博客。
*   **📊 半导体与宏观财经 (Semi Wiki & Analysis)**：重点跟进 SemiAnalysis 等半导体行业深度情报与供应链变化。
*   **🔬 前沿学术论文 (ArXiv)**：根据你的关注方向（如 Document AI、OCR、Layout Parsing 等）每日检索评估最新学术进展并进行打分。
*   **📦 代码与发布雷达 (GitHub)**：监控核心依赖库（如 LangGraph、MCP、FastAPI、Pydantic、Docling 等）的 Release，提炼破坏性更新 (Breaking Changes) 与新特性，同步抓取每日 GitHub Trending Top 10 热点。
*   **🐦 X (Twitter) 实时追踪**：通过集成 [Agent-Reach](https://github.com/Panniantong/Agent-Reach) 工具，每日自动拉取如 `@aleabitoreddit` (Serenity) 等半导体供应链/AI 硬件专家最新 10 条推文进行深度提炼。
*   **📈 雪球行情与情绪监控**：自动获取重点股票（英伟达、借壳上市标的等）和指数的实时行情，并筛选出社区内最核心的技术与产业热帖。

---

## 📁 目录结构

```text
ai-intel/
├─ config/                     # 订阅与过滤规则配置
│  ├─ feeds.yaml               # RSS 订阅源
│  ├─ watch_repos.yaml         # 监控的 GitHub 仓库
│  ├─ keywords.yaml            # 高价值重点关键词过滤
│  └─ blacklist.yaml           # 黑名单过滤规则
├─ scripts/                    # 轻量数据管道
│  ├─ collect_rss.py           # RSS 收集
│  ├─ collect_arxiv.py         # 学术论文收集
│  ├─ collect_github.py        # GitHub Release 与 Trending 收集
│  ├─ collect_xueqiu.py        # 基于 agent-reach 的雪球行情与社区爬取
│  └─ render_report.py         # 数据包聚合并渲染为 Markdown 骨架草稿
├─ skills/                     # 面向 AI Agent 的执行技能规范（SKILL.md）
│  ├─ ai-intel-briefing/       # 总编日报生成流（含 Twitter/雪球提取）
│  ├─ paper-model-radar/       # 专项论文雷达
│  └─ github-release-radar/    # 专项 Release 机会雷达
├─ Dockerfile                  # 轻量化容器环境（降级或本地运行可直接执行 python）
├─ docker-compose.yml          # 本地持久化挂载配置
└─ README.md                   # 本说明文档
```

---

## 🚀 快速上手

### 1. 准备本地 Python 环境
建议在本地使用虚拟环境（以 Windows PowerShell 举例）：
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. 配置 Agent-Reach 社交媒体凭证（可选）
本项目使用 [Agent-Reach](https://github.com/Panniantong/Agent-Reach) 作为推特和雪球的接口管理器，你需要提前在本地配置好相关凭证。
1. 安装 Agent-Reach：
   ```powershell
   pip install agent-reach
   agent-reach install --env=auto
   ```
2. 存入你的 Cookie 信息（凭证将保存在本地全局的 `~/.agent-reach/` 中，绝对不会提交至本代码仓库中）：
   *   **Twitter**：使用 Cookie-Editor 插件导出 header string，并写入本地环境变量 `TWITTER_AUTH_TOKEN` 和 `TWITTER_CT0`。
   *   **雪球**：登录雪球网，按 F12 在控制台找到 `xq_a_token`、`xq_r_token` 和 `u`，通过命令存入：
       ```powershell
       agent-reach configure xueqiu-cookies "xq_a_token=...; xq_r_token=...; u=..."
       ```

### 3. 运行数据收集管线
运行以下命令在后台静默收集今日数据并生成草稿：
```powershell
python scripts/collect_rss.py; python scripts/collect_arxiv.py; python scripts/collect_github.py; python scripts/collect_xueqiu.py; python scripts/render_report.py
```
这会在 `reports/daily/` 中产出一份 `{YYYY-MM-DD}_draft.md` 的干净骨架文件。

### 4. 由 AI 整合生成日报
如果配合 AI 助手（如 Claude Code、OpenClaw 等）使用，你可以直接呼唤它：
> **“运行 ai-intel-briefing 技能”**

AI 助手会读取生成的 `draft.md` 并调用 X (Twitter) 命令行拉取最新推特，最终为你提炼出一份精美的简报，存入你的 Obsidian 库：
`C:\Users\lidongye\Desktop\Obsidian Vault\Projects\AI 行业观察\研究笔记\`

---

## 🔒 隐私与脱敏设计

*   **Cookie 物理隔离**：雪球和 Twitter 的真实敏感 Cookie 均保存在项目目录外部（环境变量及 `~/.agent-reach/` 配置文件中），项目源码中绝不包含任何敏感密钥。
*   **本地缓存防泄露**：`.gitignore` 规则已排除了 `reports/` 目录，你的日常数据、简报日志仅保留在本地。
