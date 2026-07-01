#!/bin/bash
set -e

echo "Starting AI Intel pipeline gathering..."

echo "1. Collecting RSS feeds..."
python scripts/collect_rss.py

echo "2. Collecting ArXiv papers..."
python scripts/collect_arxiv.py || echo "Warning: ArXiv collection failed, continuing..."

echo "3. Collecting GitHub data..."
python scripts/collect_github.py || echo "Warning: GitHub collection failed, continuing..."

echo "4. Collecting Xueqiu data..."
python scripts/collect_xueqiu.py || echo "Warning: Xueqiu collection failed, continuing..."

echo "5. Rendering aggregated report..."
python scripts/render_report.py

echo "Pipeline finished successfully!"
