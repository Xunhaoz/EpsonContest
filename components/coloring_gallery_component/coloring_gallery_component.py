from components.prompt_dict import prompt_dict
from pathlib import Path

import gradio as gr


class ColoringGalleryComponent:
    def __init__(self):
        with gr.Blocks(fill_height=True) as self.index_page:
            gr.Image('static/CutPasteBanner.png', container=False, show_label=False, show_download_button=False,
                     show_fullscreen_button=False)
            with gr.Row():
                for image in Path('static/cut_paste').rglob('*.png'):
                    with gr.Column():
                        gr.Image(image, height='30vh', label=image.stem)
                        with gr.Accordion("Open for Prompt!", open=False):
                            gr.Textbox(label="Prompt", lines=10, value=prompt_dict[image.stem], show_copy_button=True)
                        gr.Button("Share Your Work!", link=f"/collect_painting?image_name={image.stem}")

    def mount(self, app, url):
        return gr.mount_gradio_app(app, self.index_page, path=url)
