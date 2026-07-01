import os
import sys
import json
import datetime

# Try to use the agent-reach venv python if we are not already in it
# This ensures it finds the agent-reach package even if run from a global python environment
try:
    from agent_reach.channels.xueqiu import XueqiuChannel
except ImportError:
    # Add virtual environment site-packages to path as fallback
    venv_path = os.path.expanduser(os.path.join("~", ".agent-reach-venv", "Lib", "site-packages"))
    if os.path.exists(venv_path) and venv_path not in sys.path:
        sys.path.append(venv_path)
    try:
        from agent_reach.channels.xueqiu import XueqiuChannel
    except ImportError:
        XueqiuChannel = None

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    reports_raw_dir = os.path.join(base_dir, 'reports', 'raw')
    os.makedirs(reports_raw_dir, exist_ok=True)
    today_str = datetime.date.today().isoformat()
    output_path = os.path.join(reports_raw_dir, f'xueqiu_{today_str}.json')

    if not XueqiuChannel:
        print("Warning: agent-reach not installed or not found in virtual environment. Skipping Xueqiu data collection.")
        # Save empty data to avoid breaking render_report
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump({"hot_posts": [], "quotes": []}, f)
        return

    print("Collecting Xueqiu data...")
    try:
        ch = XueqiuChannel()
        
        # 1. Fetch hot posts (AI & Semiconductor focus via filtering)
        print("Fetching hot posts...")
        posts = ch.get_hot_posts(limit=30)
        
        # Filter posts by keyword to focus on AI/Tech/Semiconductors
        keywords = ["AI", "智能", "芯片", "半导体", "英伟达", "NVIDIA", "比特", "BTC", "以太", "RWA", "机器人"]
        filtered_posts = []
        for p in posts:
            text_lower = (p.get("title", "") + p.get("text", "")).lower()
            if any(k.lower() in text_lower for k in keywords):
                filtered_posts.append(p)
        
        # 2. Fetch stock quotes for key tickers
        print("Fetching stock quotes...")
        tickers = ["SH000001", "SZ399001", "NVDA", "CCXI"] # Shanghai index, Shenzhen index, Nvidia, Agility Robotics SPAC
        quotes = []
        for ticker in tickers:
            try:
                q = ch.get_stock_quote(ticker)
                if q and q.get("name"):
                    quotes.append(q)
            except Exception as e:
                print(f"Error fetching quote for {ticker}: {e}")

        payload = {
            "hot_posts": filtered_posts[:10],
            "quotes": quotes
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        print(f"Saved Xueqiu data to {output_path}")

    except Exception as e:
        print(f"Error during Xueqiu collection: {e}")
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump({"hot_posts": [], "quotes": []}, f)

if __name__ == '__main__':
    main()
