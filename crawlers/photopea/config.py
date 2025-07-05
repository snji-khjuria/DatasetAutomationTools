import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from crawl4ai.async_configs import CrawlerRunConfig
documentation_run_config = CrawlerRunConfig()
documentation_run_config.exclude_external_links = True  # Exclude external links
documentation_run_config.exclude_internal_links = True  # Include internal links
documentation_run_config.exclude_all_images     = True  # Exclude all images
documentation_run_config.exclude_external_links = True  # Exclude external links



CONFIG_DETAILS="Configuration for Photopea Crawler\n\
This crawler is designed to scrape documentation, PDF datasets, and YouTube content related to Photopea"

#DOCUMENTATION CONFIG
##############################################################################################
removable_prefix_list = ["https://www.photopea.com/"]
urls_to_crawl = [{"url":"https://www.photopea.com/learn/", "banned_urls":set(["https://www.photopea.com/learn/", "https://www.photopea.com/learn"])},
            {"url":"https://www.photopea.com/tuts/", "banned_urls":set(["https://www.photopea.com/tuts/", "https://www.photopea.com/tuts"])}]


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

