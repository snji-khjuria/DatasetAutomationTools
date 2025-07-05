import os
import streamlit as st

# -------------------------------
# 🔧 Configuration
# -------------------------------
st.set_page_config(page_title="Web Crawler Config Builder", page_icon="🕷️")
st.title("🕷️ Web Crawler Config Builder")

# -------------------------------
# 📁 Utility Functions
# -------------------------------

def build_config_code(project_name, removable_prefixes_code, urls_to_crawl_code, yt_code, pdf_drive_url):
    dataset_root = os.path.join(os.path.join(".", "datasets"), project_name)
    documentation_output_dir = os.path.join(dataset_root, "documentation")
    youtube_dataset_location = os.path.join(dataset_root, "youtube_transcriptions")
    pdf_output_dir           = os.path.join(dataset_root, "pdf_dataset")

    config_lines =[                 
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from crawl4ai.async_configs import CrawlerRunConfig
documentation_run_config = CrawlerRunConfig()
documentation_run_config.exclude_external_links = True  # Exclude external links
documentation_run_config.exclude_internal_links = True  # Include internal links
documentation_run_config.exclude_all_images     = True  # Exclude all images
documentation_run_config.exclude_external_links = True  # Exclude external links\n\n\n
"""
    ]   
    config_lines += [
        f'CONFIG_DETAILS="Configuration for {project_name} Crawler\\n\\',
        f'This crawler is designed to scrape documentation, PDF datasets, and YouTube content related to {project_name}"'
    ]
    
    config_lines += [
        '# DOCUMENTATION CONFIG',
        '##############################################################################################',
        removable_prefixes_code,
        urls_to_crawl_code,
        f'documentation_output_dir = "{documentation_output_dir}"',
        '##############################################################################################',
        '\n\n\n'
    ]
    if not pdf_drive_url:
        pdf_drive_url = ""
    config_lines += [
        "#PDF DATASET CONFIG",
        "##############################################################################################",
        f'drive_url = "{pdf_drive_url}"',
        f'drive_folder_output_dir = "{pdf_output_dir}"',
        '################################################################################################',
        '\n\n\n'
    ]
    config_lines += [
        '#YOUTUBE CONTENT CONFIG',
        '##############################################################################################',
        yt_code,
        f'youtube_dataset_location = "{youtube_dataset_location}"',
        '###############################################################################################\n\n\n'
    ]
    return "\n".join(config_lines)


def init_session():
    if "pdf_confirmed" not in st.session_state:
        st.session_state.pdf_confirmed = False
    if "yt_playlists" not in st.session_state:
        st.session_state.yt_playlists = []
    if "removable_prefixes" not in st.session_state:
        st.session_state.removable_prefixes = []
    if "urls_to_crawl" not in st.session_state:
        st.session_state.urls_to_crawl = []

def show_removable_prefix_input():
    st.markdown("### 🔁 Removable URL Prefixes")
    new_prefix = st.text_input("Add Removable Prefix", key="prefix_input")
    st.caption("🧹 These are URL prefixes you want to strip when saving files — e.g., removing `https://www.photopea.com/` will remove this prefix")
    if st.button("➕ Add Prefix"):
        if new_prefix.strip():
            st.session_state.removable_prefixes.append(new_prefix.strip())
            st.success(f"Added prefix: {new_prefix.strip()}")
        else:
            st.warning("Please enter a valid URL prefix.")
    
    removable_prefix_code = "removable_prefix_list = [\n"
    for prefix in st.session_state.removable_prefixes:
        removable_prefix_code += f'    "{prefix}",\n'
    removable_prefix_code += "]"

    if st.session_state.removable_prefixes:
        st.markdown("#### ✅ Current Prefixes:")
        st.code(removable_prefix_code, language='python')
    return removable_prefix_code

def show_url_crawl_input():
    st.markdown("### 🌐 URLs to Crawl")
    crawl_url = st.text_input("Crawl URL", key="crawl_url")
    banned_urls = st.text_area(
        "Banned URLs (comma-separated)", key="banned_urls_input",
        placeholder="Enter comma-separated banned URLs"
    )
    st.caption("❌ Banned URLs are pages you don’t want to save. For example, to crawl everything under `photopea.com/learn/` but skip saving `photopea.com/learn/`, add `https://www.photopea.com/learn/` here.")
    if st.button("➕ Add Crawl Entry"):
        if crawl_url.strip():
            banned_set = set([url.strip() for url in banned_urls.split(",") if url.strip()])
            st.session_state.urls_to_crawl.append({
                "url": crawl_url.strip(),
                "banned_urls": banned_set
            })
            st.success(f"Added crawl URL: {crawl_url.strip()} with {len(banned_set)} banned URLs.")
        else:
            st.warning("Crawl URL cannot be empty.")
    urls_to_crawl_code = "urls_to_crawl = [\n"
    for entry in st.session_state.urls_to_crawl:
        urls_to_crawl_code += f'    {{"url": "{entry["url"]}", "banned_urls": set({entry["banned_urls"]})}},\n'
    urls_to_crawl_code += "]"
    if st.session_state.urls_to_crawl:
        st.markdown("#### ✅ Current Crawl URLs:")
        st.code(urls_to_crawl_code, language='python')
    return urls_to_crawl_code

def show_pdf_input():
    st.markdown("### ➕ PDF Dataset")
    pdf_drive_url = st.text_input("Google Drive Folder URL")

    if st.button("✅ Confirm PDF Link"):
        if pdf_drive_url.strip():
            st.session_state.pdf_confirmed = True
        else:
            st.session_state.pdf_confirmed = False
            st.warning("Please enter a valid Google Drive folder URL before confirming.")

    if st.session_state.pdf_confirmed:
        st.success(f"✅ This Drive link will be used to fetch the PDF dataset:\n{pdf_drive_url.strip()}")
    
    return pdf_drive_url.strip()


def show_youtube_input():
    st.markdown("### ➕ Add YouTube Playlist")
    col1, col2 = st.columns(2)
    with col1:
        yt_name = st.text_input("Channel Name", key="yt_name")
    with col2:
        yt_url = st.text_input("Playlist URL", key="yt_url")

    if st.button("➕ Add to Playlist List"):
        if yt_name.strip() and yt_url.strip():
            st.session_state.yt_playlists.append((yt_name.strip(), yt_url.strip()))
            st.success(f"Added: {yt_name.strip()} → {yt_url.strip()}")
        else:
            st.warning("Please fill both Channel Name and Playlist URL.")

    yt_code = "youtube_playlists = [\n"
    for name, url in st.session_state.yt_playlists:
        yt_code += f'    ("{name}", "{url}"),\n'
    yt_code += "]"

    if st.session_state.yt_playlists:
        st.markdown("#### ✅ Current Playlist Entries:")
        st.code(yt_code, language='python')
    
    return yt_code


def generate_config(project_name, removable_prefixes_code, urls_to_crawl_code, yt_code, pdf_drive_url):
    if not project_name.strip():
        st.warning("⚠️ Please enter a valid project name.")
        return

    crawler_path = os.path.join("./crawlers", project_name.strip())
    if os.path.exists(crawler_path):
        st.warning(f"⚠️ Folder `{crawler_path}` already exists. Please delete it first before generating a new config.")
    else:
        try:
            os.makedirs(crawler_path)
            config_code = build_config_code(project_name.strip(), removable_prefixes_code, urls_to_crawl_code, yt_code, pdf_drive_url)
            config_path = os.path.join(crawler_path, "config.py")
            with open(config_path, "w") as f:
                f.write(config_code)
            st.success(f"✅ Folder `{crawler_path}` created with `config.py`.")
        except Exception as e:
            st.error(f"❌ Error while generating config: {e}")


# -------------------------------
# 🧠 Main UI Logic
# -------------------------------
init_session()
project_name        = st.text_input("Enter website or project name (e.g., `zomato`, `photoshop`, `photopea`)")
pdf_drive_url       = show_pdf_input()
yt_code             = show_youtube_input()
urls_to_crawl_code       = show_url_crawl_input()
removable_prefixes_code  = show_removable_prefix_input()
st.markdown("---")
st.markdown("## 🛠️ Final Step")
st.markdown("Once all inputs are ready, click below to generate the configuration file.")
st.markdown("")

if st.button("🚀 Generate Configuration"):
    generate_config(project_name, removable_prefixes_code, urls_to_crawl_code, yt_code, pdf_drive_url)
