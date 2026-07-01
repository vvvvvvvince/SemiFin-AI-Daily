---
name: ai-intel
description: 个人 AI 情报系统根 Skill，负责编排每日日报、学术论文雷达及 GitHub 发布雷达的运行。
---

# AI Intel 个人情报系统

## 概述
这是一个部署在本地的 AI/Agent 研发情报聚合与提炼系统。结构为 **“1个总编日报 Skill + 2个专项雷达 + 1个数据管道”**，旨在减少低质信息噪音，输出具备高度项目关联和可执行性的技术日报。

## 目录结构
```
ai-intel/
├─ skills/
│  ├─ ai-intel-briefing/       # 总编日报 Skill
│  │  └─ SKILL.md
│  ├─ paper-model-radar/       # 论文与模型雷达 Skill
│  │  └─ SKILL.md
│  └─ github-release-radar/    # 开发机会雷达 Skill
│     └─ SKILL.md
├─ config/
│  ├─ feeds.yaml               # RSS 订阅源配置
│  ├─ watch_repos.yaml         # GitHub 关注仓库
│  ├─ keywords.yaml            # 高价值重点过滤词
│  └─ blacklist.yaml           # 黑名单过滤词
├─ reports/
│  ├─ raw/                     # 原始聚合 JSON 数据
│  └─ daily/                   # 本地 Markdown 备份草稿
├─ scripts/
│  ├─ collect_rss.py           # RSS 收集脚本
│  ├─ collect_arxiv.py         # 学术论文收集脚本
│  ├─ collect_github.py        # GitHub 变更收集脚本
│  └─ render_report.py         # 数据包汇总脚本
└─ SKILL.md                    # 本手册
```

## 使用说明

当需要生成日报时，可指示 Agent 执行以下任意一个技能：
1. **总编日报** (`ai-intel-briefing`)：生成全网 AI 动态与项目落地建议。
2. **论文模型雷达** (`paper-model-radar`)：筛选重点关键词（如 OCR, Layout Parsing 等）相关的最新学术成果。
3. **开发机会雷达** (`github-release-radar`)：检查核心依赖库（如 LangGraph, Pydantic 等）的破坏性更新与可复用新特性。

可以通过 `/schedule` 挂载每日定时调度。
