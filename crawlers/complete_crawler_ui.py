import os
import importlib
import asyncio
import gradio as gr

from utils import process_url_list, download_drive_folder, get_all_documentation_links
from youtube_utils import prepare_youtube_dataset

# Get available config folders
def get_config_folders():
    crawlers_path = "crawlers"
    return [
        name for name in os.listdir(crawlers_path)
        if os.path.isdir(os.path.join(crawlers_path, name)) and os.path.exists(os.path.join(crawlers_path, name, "config.py"))
    ]

def run_pipeline(config_name, run_doc, run_pdf, run_yt):
    logs = ""

    try:
        config_module = importlib.import_module(f"{config_name}.config")

        removable_prefix_list = config_module.removable_prefix_list
        urls_to_crawl = config_module.urls_to_crawl
        documentation_run_config = config_module.documentation_run_config
        documentation_output_dir = config_module.documentation_output_dir

        drive_url = config_module.drive_url
        drive_folder_output_dir = config_module.drive_folder_output_dir

        youtube_playlists = config_module.youtube_playlists
        youtube_dataset_location = config_module.youtube_dataset_location
        CONFIG_DETAILS = config_module.CONFIG_DETAILS

        logs += f"✔️ Loaded config: {config_name}\n"
        yield logs

        if run_doc:
            logs += "📄 Downloading documentation...\n"
            yield logs

            all_links = get_all_documentation_links(urls_to_crawl)
            logs += f"Found {len(all_links)} documentation URLs...\n"
            yield logs

            asyncio.run(process_url_list(all_links, removable_prefix_list, documentation_run_config, output_dir=documentation_output_dir))
            logs += f"✅ Documentation saved to: {documentation_output_dir}\n"
            yield logs

        if run_pdf:
            logs += "📚 Downloading PDFs...\n"
            yield logs

            download_drive_folder(drive_url=drive_url, local_folder=drive_folder_output_dir)
            logs += f"✅ PDFs saved to: {drive_folder_output_dir}\n"
            yield logs

        if run_yt:
            logs += "🎥 Downloading YouTube videos...\n"
            yield logs

            prepare_youtube_dataset(youtube_dataset_location, youtube_playlists)
            logs += f"✅ YouTube dataset saved to: {youtube_dataset_location}\n"
            yield logs

        logs += "🎉 All tasks completed!\n"
        yield logs

    except Exception as e:
        logs += f"❌ Error: {str(e)}\n"
        yield logs

css="""
.gradio-container {
    display: flex;
    justify-content: center;
    justify-content: center;
    align-items: center;
}

#component-0 {
    width: 100%;
    max-width: 1200px;
    padding: 50px;
    padding-left:30%;
    box-sizing: border-box;
    overflow-x: hidden;
    justify-content: center;
    align-items: center;
}

.gr-textbox textarea {
    width: 100% !important;
    box-sizing: border-box;
    resize: vertical;
    justify-content: center;
    align-items: center;
}
"""
# Gradio UI
with gr.Blocks(css=css) as demo:
    gr.Markdown("## 📡 Crawler UI")

    config_folders = get_config_folders()
    config_choice = gr.Dropdown(choices=config_folders, label="Select Config Folder")

    run_doc = gr.Checkbox(label="📄 Download Documentation", value=True)
    run_pdf = gr.Checkbox(label="📚 Download PDFs", value=True)
    run_yt = gr.Checkbox(label="🎥 Download YouTube Videos", value=True)

    run_button = gr.Button("🚀 Run Crawler")
    output_box = gr.Textbox(label="Output", lines=10, interactive=False)

    run_button.click(fn=run_pipeline, inputs=[config_choice, run_doc, run_pdf, run_yt], outputs=output_box)


# Run the Gradio app
if __name__ == "__main__":
    demo.launch()
