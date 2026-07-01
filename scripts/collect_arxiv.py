import os
import sys
import json
import datetime
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import argparse

try:
    import yaml
except ImportError:
    print("Error: pyyaml package is required. Install it using 'pip install pyyaml'")
    sys.exit(1)

def load_config(config_path):
    if not os.path.exists(config_path):
        return {}
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def parse_arxiv_xml(xml_data):
    root = ET.fromstring(xml_data)
    namespace = {'atom': 'http://www.w3.org/2005/Atom'}
    
    entries = []
    for entry in root.findall('atom:entry', namespace):
        title = entry.find('atom:title', namespace)
        title_text = title.text.strip().replace('\n', ' ') if title is not None else ""
        
        summary = entry.find('atom:summary', namespace)
        summary_text = summary.text.strip().replace('\n', ' ') if summary is not None else ""
        
        id_url = entry.find('atom:id', namespace)
        link_text = id_url.text.strip() if id_url is not None else ""
        
        published = entry.find('atom:published', namespace)
        pub_date = published.text.strip() if published is not None else ""
        
        authors = []
        for author in entry.findall('atom:author', namespace):
            name = author.find('atom:name', namespace)
            if name is not None:
                authors.append(name.text.strip())
                
        entries.append({
            "title": title_text,
            "summary": summary_text,
            "link": link_text,
            "published": pub_date,
            "authors": authors
        })
    return entries

def match_keywords(entry, keywords):
    score = 0
    text = (entry['title'] + " " + entry['summary']).lower()
    matched = []
    for kw in keywords:
        if kw.lower() in text:
            score += 1
            matched.append(kw)
    return score, matched

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true', help='Dry run execution')
    args = parser.parse_args()

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_dir = os.path.join(base_dir, 'config')
    reports_dir = os.path.join(base_dir, 'reports', 'raw')
    os.makedirs(reports_dir, exist_ok=True)

    keywords = load_config(os.path.join(config_dir, 'keywords.yaml')).get('keywords', [])
    today_str = datetime.date.today().isoformat()

    results = []

    if args.dry_run:
        print("Dry run mode: using mock papers")
        results.append({
            "title": "Document AI and Layout Parsing: A Survey",
            "summary": "This paper presents a comprehensive review of layout parsing methods for PDF extraction in document AI pipelines.",
            "link": "http://arxiv.org/abs/mock.12345",
            "published": today_str,
            "authors": ["Author One", "Author Two"],
            "score": 3,
            "matched_keywords": ["document AI", "layout parsing", "PDF extraction"]
        })
    else:
        query = 'cat:cs.AI OR cat:cs.LG OR cat:cs.CL'
        url = f'http://export.arxiv.org/api/query?search_query={urllib.parse.quote(query)}&sortBy=submittedDate&sortOrder=descending&max_results=50'
        
        print(f"Querying ArXiv API: {url}")
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Antigravity AI Daily Client'})
            import ssl
            context = ssl._create_unverified_context()
            with urllib.request.urlopen(req, context=context) as response:
                xml_data = response.read()
            
            entries = parse_arxiv_xml(xml_data)
            print(f"Fetched {len(entries)} papers from ArXiv. Filtering with keywords...")
            
            for entry in entries:
                score, matched = match_keywords(entry, keywords)
                if score > 0:
                    entry['score'] = score
                    entry['matched_keywords'] = matched
                    results.append(entry)
                    
            results.sort(key=lambda x: x['score'], reverse=True)
            print(f"Found {len(results)} papers matching keywords.")
        except Exception as e:
            print(f"Error querying ArXiv: {e}")

    output_path = os.path.join(reports_dir, f'arxiv_{today_str}.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"Saved ArXiv data to {output_path}")

if __name__ == '__main__':
    main()
