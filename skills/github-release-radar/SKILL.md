---
name: github-release-radar
description: 关注仓库 Release、Issue、Commit、热门项目的开发与机会发现雷达。
---

# github-release-radar 开发机会雷达

## 概述
追踪关注代码库的版本迭代变化，提炼对现有开发工作有实质影响的 Release，重点筛出破坏性变更 (Breaking Changes) 以及可以减少手写工作量的新能力。

## 工作流

### 第一步：获取 GitHub 最新数据
1. 在项目根目录下运行：
   `python scripts/collect_github.py`

### 第二步：分析变更与机会
1. 读取 `reports/raw/github_{YYYY-MM-DD}.json`。
2. 利用大模型对这几类变更进行分级提炼：
   - **Release 追踪**：说明哪些项目发布了新版，是否有升级必要。
   - **Breaking Change**：警告可能影响当前项目平稳运行的破坏性修改。
   - **New Capability**：提取可能减少目前开发工作量的内置新特性。

### 第三步：生成报告
按以下结构化格式生成报告：

```markdown
---
title: {YYYY-MM-DD} GitHub开发雷达
project: AI 行业观察
type: 工具选型
tags: [github, release-radar, dev-ops]
date: {YYYY-MM-DD}
source: Antigravity开发雷达
status: 📝草稿
---

# GitHub Release Radar — {YYYY-MM-DD}

## 核心推送 (今日值得关注的更新)

### 1. {仓库名} - {新版本号}
- **升级建议**：[推荐升级 / 暂缓 / 仅作了解]
- **Breaking Change**：{列出，若无则写“无”}
- **新能力提炼**：{说明此版本带来了什么新特性，能否减少我们的业务手写量}
- **参考链接**：[{版本说明页}]({url})
```

### 第四步：写入 Obsidian
1. 保存至：`C:\Users\lidongye\Desktop\Obsidian Vault\Projects\AI 行业观察\研究笔记\{YYYY-MM-DD}_Github_Radar.md`。
