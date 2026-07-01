---
name: paper-model-radar
description: 论文、模型、评测、Hugging Face 热点追踪雷达。
---

# paper-model-radar 论文与模型雷达

## 概述
专注于挖掘前沿学术研究与开源权重模型，尤其是与 Document AI, OCR, Layout Parsing, 医药研发等强相关的领域。

## 工作流

### 第一步：获取论文数据
1. 在项目根目录下运行：
   `python scripts/collect_arxiv.py`

### 第二步：分析与评估
1. 读取 `reports/raw/arxiv_{YYYY-MM-DD}.json`。
2. 结合 `config/keywords.yaml` 过滤相关论文。
3. 利用大模型整理为如下结构化评估：

```markdown
---
title: {YYYY-MM-DD} 论文与模型雷达
project: AI 行业观察
type: 研究笔记
tags: [arxiv, paper-radar, document-ai, ocr]
date: {YYYY-MM-DD}
source: Antigravity论文雷达
status: 📝草稿
---

# Paper & Model Radar — {YYYY-MM-DD}

## 今日值得看
### 1. {论文 / 模型名称}
- **解决什么问题**：{简述}
- **是否有开源代码/权重**：{是/否，附链接}
- **应用场景评估**：{是否能用于 Agent / PDF / OCR / 企业私有化部署 / 医药 AI}
- **行动建议**：[看 / 收藏 / 跳过]

## 本周推荐复现 (最多 1 个)
- **项目/模型**：{名称}
- **最小 PoC 路径**：{说明如何用 10 行以内的代码或命令进行初步本地跑通测试}
```

### 第三步：写入 Obsidian
1. 检查是否存在路径：`C:\Users\lidongye\Desktop\Obsidian Vault\Projects\AI 行业观察\研究笔记\`。
2. 保存为：`C:\Users\lidongye\Desktop\Obsidian Vault\Projects\AI 行业观察\研究笔记\{YYYY-MM-DD}_Paper_Radar.md`。
