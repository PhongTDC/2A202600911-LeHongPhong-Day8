import asyncio
import os
import json
from datetime import datetime
from crawl4ai import AsyncWebCrawler

URLS = [
    "https://example-news.com/nghe-si-a-ma-tuy",
]

async def crawl_article(url: str, output_dir: str = "data/landing/news"):
    os.makedirs(output_dir, exist_ok=True)
    filename = url.split("/")[-1] or f"news_{int(datetime.now().timestamp())}"
    output_path = os.path.join(output_dir, f"{filename}.json")
    
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url=url)
        
        article_data = {
            "metadata": {
                "url": url,
                "crawl_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "title": result.metadata.get("title", "No Title") if result.metadata else "No Title"
            },
            "markdown": result.markdown
        }
        
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(article_data, f, ensure_ascii=False, indent=4)
    print(f"✓ Crawled & Saved: {output_path}")

async def main():
    for url in URLS:
        try:
            await crawl_article(url)
        except Exception as e:
            print(f"Error crawling {url}: {e}")

if __name__ == "__main__":
    asyncio.run(main())
