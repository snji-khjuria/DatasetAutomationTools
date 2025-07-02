import sys
import os
import asyncio
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from crawlers.utils import download_drive_folder

drive_url = "https://drive.google.com/drive/folders/1Wns1ifFYmapP4dOFW2qn1M7yhQaLujkF?usp=sharing"

download_drive_folder(drive_url=drive_url, local_folder="./datasets/photopea/pdf_dataset")

