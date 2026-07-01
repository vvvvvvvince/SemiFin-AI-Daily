import os
import sys
import json
import datetime
import argparse

def load_json(filepath):
    if not os.path.exists(filepath):
        return {}
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return {}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mock', action='store_true', help='Use mock data')
    args = parser.parse_args()

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    reports_raw_dir = os.path.join(base_dir, 'reports', 'raw')
    reports_daily_dir = os.path.join(base_dir, 'reports', 'daily')
    os.makedirs(reports_daily_dir, exist_ok=True)

    today_str = datetime.date.today().isoformat()

    rss_data = {}
    arxiv_data = []
    github_data = {}
    xueqiu_data = {}

    if args.mock:
        print("Mock mode: Loading dry-run data")
        rss_data = {
            "official_labs": [{
                "feed_name": "Mock Lab",
                "title": "Mock Article about Document AI and OCR",
                "link": "http://example.com/mock",
                "summary": "This is a mock summary of a very interesting document AI development.",
                "published": today_str
            }]
        }
        arxiv_data = [{
            "title": "Document AI and Layout Parsing: A Survey",
            "summary": "This paper presents a comprehensive review of layout parsing methods for PDF extraction in document AI pipelines.",
            "link": "http://arxiv.org/abs/mock.12345",
            "published": today_str,
            "authors": ["Author One", "Author Two"],
            "score": 3,
            "matched_keywords": ["document AI", "layout parsing", "PDF extraction"]
        }]
        github_data = {
            "releases": [{
                "repo": "modelcontextprotocol/specification",
                "tag_name": "v0.5.0",
                "name": "MCP Specification Update",
                "published_at": today_str,
                "html_url": "https://github.com/modelcontextprotocol/specification/releases/tag/v0.5.0",
                "body": "### Breaking Changes\n- Updated authentication scheme in security spec.\n### New Capabilities\n- Added layout-parsing schema support."
            }],
            "trending": [{
                "rank": 1,
                "repo": "browser-use/video-use",
                "url": "https://github.com/browser-use/video-use",
                "description": "Edit videos with coding agents"
            }]
        }
        xueqiu_data = {
            "quotes": [{
                "symbol": "SH000001",
                "name": "上证指数",
                "current": 3000.0,
                "percent": 0.5
            }],
            "hot_posts": [{
                "title": "AI芯片发展趋势",
                "url": "https://xueqiu.com/123",
                "author": "投资大咖",
                "text": "随着算力需求增加，AI芯片公司利润将持续增长。"
            }]
        }
    else:
        rss_data = load_json(os.path.join(reports_raw_dir, f'rss_{today_str}.json'))
        arxiv_data = load_json(os.path.join(reports_raw_dir, f'arxiv_{today_str}.json'))
        github_data = load_json(os.path.join(reports_raw_dir, f'github_{today_str}.json'))
        xueqiu_data = load_json(os.path.join(reports_raw_dir, f'xueqiu_{today_str}.json'))

    # Compile aggregated payload
    aggregated = {
        "date": today_str,
        "rss": rss_data,
        "arxiv": arxiv_data,
        "github": github_data,
        "xueqiu": xueqiu_data
    }

    aggregated_path = os.path.join(reports_raw_dir, f'aggregated_{today_str}.json')
    with open(aggregated_path, 'w', encoding='utf-8') as f:
        json.dump(aggregated, f, ensure_ascii=False, indent=2)
    print(f"Saved aggregated JSON payload to {aggregated_path}")

    # Generate basic draft markdown report (fallback/direct output)
    draft_content = []
    draft_content.append(f"# AI Daily Raw Gather - {today_str}\n")
    
    draft_content.append("## RSS Feeds")
    if rss_data:
        for cat, items in rss_data.items():
            draft_content.append(f"### Category: {cat}")
            for item in items:
                draft_content.append(f"- **[{item['title']}]({item['link']})** ({item['feed_name']})")
                draft_content.append(f"  {item.get('summary', '')[:300]}")
    else:
        draft_content.append("No RSS feed updates found.")

    draft_content.append("\n## ArXiv Papers")
    if arxiv_data:
        for paper in arxiv_data:
            draft_content.append(f"### [{paper['title']}]({paper['link']})")
            draft_content.append(f"- **Score**: {paper.get('score', 0)} | **Matched**: {', '.join(paper.get('matched_keywords', []))}")
            draft_content.append(f"- **Authors**: {', '.join(paper.get('authors', []))}")
            draft_content.append(f"  {paper.get('summary', '')[:400]}")
    else:
        draft_content.append("No matching ArXiv papers found.")

    # Parse GitHub Releases and Trending
    releases = []
    trending = []
    if isinstance(github_data, dict):
        releases = github_data.get("releases", [])
        trending = github_data.get("trending", [])
    else:
        releases = github_data

    draft_content.append("\n## GitHub Releases")
    if releases:
        for release in releases:
            draft_content.append(f"### [{release['repo']} - {release['tag_name']}]({release['html_url']})")
            draft_content.append(f"  {release.get('body', '')[:500]}")
    else:
        draft_content.append("No GitHub releases found.")

    draft_content.append("\n## GitHub Daily Trending Top 10")
    if trending:
        for item in trending:
            draft_content.append(f"### {item['rank']}. [{item['repo']}]({item['url']})")
            draft_content.append(f"  {item['description']}")
    else:
        draft_content.append("No GitHub trending items found.")

    draft_content.append("\n## Xueqiu Tickers & Hot Posts")
    xq_quotes = xueqiu_data.get("quotes", []) if isinstance(xueqiu_data, dict) else []
    xq_posts = xueqiu_data.get("hot_posts", []) if isinstance(xueqiu_data, dict) else []

    if xq_quotes:
        draft_content.append("### Quotes")
        for q in xq_quotes:
            draft_content.append(f"- **{q.get('name')} ({q.get('symbol')})**: {q.get('current')} ({q.get('percent')}%)")

    if xq_posts:
        draft_content.append("### Hot Posts")
        for p in xq_posts:
            title_text = p.get('title') or '无标题'
            draft_content.append(f"- **[{title_text}]({p.get('url')})** (@{p.get('author')})")
            draft_content.append(f"  {p.get('text', '')}")
    else:
        draft_content.append("No Xueqiu data found.")

    draft_path = os.path.join(reports_daily_dir, f'{today_str}_draft.md')
    with open(draft_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(draft_content))
    print(f"Saved raw markdown draft to {draft_path}")

if __name__ == '__main__':
    main()
