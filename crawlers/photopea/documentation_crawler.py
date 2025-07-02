import sys
import os
import asyncio
from crawl4ai.async_configs import CrawlerRunConfig


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from crawlers.utils import extract_urls, process_url_list
learn_prefix = "https://www.photopea.com/learn/"
learn_banned_urls = {"https://www.photopea.com/learn/", "https://www.photopea.com/learn"}
learn_url_info = (learn_prefix, learn_banned_urls)

tutorials_prefix = "https://www.photopea.com/tuts/"
tutorials_banned_urls = {"https://www.photopea.com/tuts/", "https://www.photopea.com/tuts"}
tutorial_url_info = (tutorials_prefix, tutorials_banned_urls)

removable_prefix_list = ["https://www.photopea.com/"]


all_learn_links     = extract_urls("https://www.photopea.com/learn/", learn_url_info)
all_tutorials_links = extract_urls("https://www.photopea.com/tuts/", tutorial_url_info)
all_links = all_learn_links + all_tutorials_links




print("Total Learn URLs found:", len(all_learn_links))
print("Total Tutorials URLs found:", len(all_tutorials_links))
print("Total URLs found:", len(all_links))

run_config = CrawlerRunConfig()
run_config.exclude_external_links = True  # Exclude external links
run_config.exclude_internal_links = True  # Include internal links
run_config.exclude_all_images = True  # Exclude all images
run_config.exclude_external_links = True  # Exclude external links

asyncio.run(process_url_list(all_links, removable_prefix_list, run_config, output_dir="./datasets/photopea/documentation"))
