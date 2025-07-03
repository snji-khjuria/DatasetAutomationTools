import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))



CONFIG_DETAILS="Configuration for Photopea Crawler\n\
This crawler is designed to scrape documentation, PDF datasets, and YouTube content related to Photopea"


#DOCUMENTATION CONFIG
##############################################################################################
from crawlers.utils import extract_urls
from crawl4ai.async_configs import CrawlerRunConfig


removable_prefix_list = ["https://www.photopea.com/"]

learn_prefix          = "https://www.photopea.com/learn/"
learn_banned_urls     = {"https://www.photopea.com/learn/", "https://www.photopea.com/learn"}
learn_url_info        = (learn_prefix, learn_banned_urls)

tutorials_prefix      = "https://www.photopea.com/tuts/"
tutorials_banned_urls = {"https://www.photopea.com/tuts/", "https://www.photopea.com/tuts"}
tutorial_url_info     = (tutorials_prefix, tutorials_banned_urls)

def get_all_documentation_links():
    """Extract all links from the Photopea learn and tutorials pages."""
    all_learn_links = extract_urls("https://www.photopea.com/learn/", learn_url_info)
    all_tutorials_links = extract_urls("https://www.photopea.com/tuts/", tutorial_url_info)
    return all_learn_links + all_tutorials_links

documentation_run_config = CrawlerRunConfig()
documentation_run_config.exclude_external_links = True  # Exclude external links
documentation_run_config.exclude_internal_links = True  # Include internal links
documentation_run_config.exclude_all_images = True  # Exclude all images
documentation_run_config.exclude_external_links = True  # Exclude external links


documentation_output_dir = "./datasets/photopea/documentation"
###############################################################################################


#PDF DATASET CONFIG
##############################################################################################
drive_url = "https://drive.google.com/drive/folders/1Wns1ifFYmapP4dOFW2qn1M7yhQaLujkF?usp=sharing"
drive_folder_output_dir = "./datasets/photopea/pdf_dataset"
################################################################################################



#YOUTUBE CONTENT CONFIG
##############################################################################################
youtube_playlists = [
                    # ("fNd", "https://www.youtube.com/playlist?list=PLvNXvOQ8ylUU9C7gzA1Xtg79KBmlAKghh"),
                    #  ("techSupport", "https://www.youtube.com/playlist?list=PLqWGp356JsNvKFTNgvvNfYfVdOs_M9EYv"),
                    #  ("kruMark", "https://www.youtube.com/playlist?list=PL5fmsRtjcmExeJFmoBsTtFL0vnj4g5xj7"),
                    #  ("Adomi", "https://www.youtube.com/playlist?list=PLCMGVxg-SSzV30nX9HWAIAacfY6-gHDdR"),
                     ("Auri", "https://www.youtube.com/playlist?list=PLWo9muNw-oVRujzM_sF2TnIEz_4sQsAL-"),
                    #  ("Cambit", "https://www.youtube.com/playlist?list=PLwkbAxcLGld2hVwe0Kt_t358E4z_E2bE8")
                    ]
youtube_dataset_location = "./datasets/photopea/youtube_transcriptions"

###############################################################################################

