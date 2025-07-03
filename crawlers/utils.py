import asyncio
from crawl4ai import AsyncWebCrawler
from urllib.parse import urlparse
import re
import os
import asyncio
import shutil
from crawl4ai import AsyncWebCrawler
from crawl4ai.async_configs import BrowserConfig, CrawlerRunConfig
import os
import shutil
import gdown

def extract_urls(url, url_info):
    approved_prefix, banned_urls = url_info
    """Extract all URLs from a given web page using crawl4ai."""
    async def _extract():
        async with AsyncWebCrawler() as crawler:
            result = await crawler.arun(url=url)
            links = result.links
            if not links:
                print(f"No links found on the page: {url}")
                return []
            internal_links = [k["href"] for k in links.get("internal", []) if k["href"].startswith(approved_prefix)]
            external_links = [k["href"] for k in links.get("external", []) if k["href"].startswith(approved_prefix)]
            total_urls = internal_links + external_links
            total_urls = [url for url in total_urls if url not in banned_urls]
            return list(set(total_urls))
    return asyncio.run(_extract())



def sanitize_filename(url, removable_prefix_list):
    #remove prefix if present from any of the removable prefixes_list
    for prefix in removable_prefix_list:
        if url.startswith(prefix):
            url = url[len(prefix):]
    # Replace all non-alphanumeric characters with underscores
    return re.sub(r'[^a-zA-Z0-9]', '_', url)




async def save_text_from_url(url, removable_prefix_list, output_dir, crawler=None, run_config=None):
    try:
        result = await crawler.arun(url=url, config=run_config)
        text = result.markdown
    except Exception as e:
        print(f"❌ Failed to load {url}: {e}")
        return

    filename = sanitize_filename(url, removable_prefix_list) + ".txt"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(text)

    print(f"✅ Saved: {filepath}")



async def process_url_list(url_list, removable_prefix_list, run_config, output_dir):
    browser_config = BrowserConfig()

    # Remove entire output directory if it exists
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    async with AsyncWebCrawler(config=browser_config) as crawler:
        tasks = [save_text_from_url(url, removable_prefix_list, output_dir, crawler, run_config) for url in url_list]
        await asyncio.gather(*tasks)



def download_drive_folder(drive_url: str, local_folder: str):
    # Delete the folder if it exists
    if os.path.exists(local_folder):
        shutil.rmtree(local_folder)
    os.makedirs(local_folder, exist_ok=True)

    # Extract folder ID from the Google Drive folder URL
    if "folders/" in drive_url:
        folder_id = drive_url.split("folders/")[1].split("?")[0]
    else:
        raise ValueError("Invalid folder link. Must be of the form: https://drive.google.com/drive/folders/<FOLDER_ID>")

    # gdown format to download folders
    gdown.download_folder(f"https://drive.google.com/drive/folders/{folder_id}", output=local_folder, quiet=False, use_cookies=False)

    print(f"All files downloaded to: {local_folder}")


