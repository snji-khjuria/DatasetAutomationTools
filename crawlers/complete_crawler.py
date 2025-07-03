import asyncio
import argparse
from utils import process_url_list, download_drive_folder
from youtube_utils import prepare_youtube_dataset

parser = argparse.ArgumentParser(description="Complete Crawler")
#python complete_crawler.py --config photopea
parser.add_argument('--config', type=str, required=True, help='Specify the config name (e.g., photopea)')

parser.add_argument('--documentation', dest='documentation', action='store_true', help='Enable documentation download')
parser.add_argument('--no-documentation', dest='documentation', action='store_false', help='Disable documentation download')

parser.add_argument('--pdf', dest='pdf', action='store_true', help='Enable PDF download')
parser.add_argument('--no-pdf', dest='pdf', action='store_false', help='Disable PDF download')

parser.add_argument('--youtube', dest='youtube', action='store_true', help='Enable YouTube download')
parser.add_argument('--no-youtube', dest='youtube', action='store_false', help='Disable YouTube download')

parser.set_defaults(documentation=True, pdf=True, youtube=True)

args = parser.parse_args()

documentation = args.documentation
pdf = args.pdf
youtube = args.youtube


import importlib
config_module = importlib.import_module(f"{args.config}.config")
removable_prefix_list       = config_module.removable_prefix_list
get_all_documentation_links = config_module.get_all_documentation_links
documentation_run_config    = config_module.documentation_run_config
documentation_output_dir    = config_module.documentation_output_dir

drive_url                   = config_module.drive_url
drive_folder_output_dir     = config_module.drive_folder_output_dir

youtube_playlists           = config_module.youtube_playlists
youtube_dataset_location    = config_module.youtube_dataset_location
CONFIG_DETAILS              = config_module.CONFIG_DETAILS


print(CONFIG_DETAILS)
print("Documentation:", args.documentation)
print("PDF:", args.pdf)
print("YouTube:", args.youtube)
if documentation:
    print("Starting the documentation dataset downloader script.")
    all_links = get_all_documentation_links()
    print("Total URLs found:", len(all_links))
    asyncio.run(process_url_list(all_links, removable_prefix_list, documentation_run_config, output_dir=documentation_output_dir))
    print("Documentation dataset downloaded successfully.")
    print("You can find the dataset in the folder:", documentation_output_dir)

if pdf:
    print("Running the PDF dataset downloader script to download the PDF dataset.")
    download_drive_folder(drive_url=drive_url, local_folder=drive_folder_output_dir)
    print("PDF dataset downloaded successfully.")
    print("You can find the PDF dataset in the folder:", drive_folder_output_dir)

if youtube:
    print("Running the YouTube content crawler script to download the YouTube content dataset.")
    prepare_youtube_dataset(youtube_dataset_location, youtube_playlists)
    print("YouTube content dataset downloaded successfully.")
    print("You can find the YouTube content dataset in the folder:", youtube_dataset_location)