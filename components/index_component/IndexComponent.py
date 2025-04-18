import gradio as gr


class IndexComponent:
    head = """
    <style>
    .gallery_cover {
        border-radius: 20px !important;
    }
    </style>
    """

    def __init__(self):
        with gr.Blocks(fill_height=True, head=self.head) as self.index_page:
            gr.Image('static/index.png', container=False, show_label=False, show_download_button=False, show_fullscreen_button=False)

            with gr.Row():
                with gr.Column():
                    gr.Image(
                        'static/cut_paste_cover.jpg', elem_classes="gallery_cover",
                        container=False, show_label=False, show_download_button=False, show_fullscreen_button=False)
                    gr.Button("查看更多!!", link="/coloring_gallery")
                with gr.Column():
                    gr.Image(
                        'static/coloring_cover.jpg', elem_classes="gallery_cover",
                        container=False, show_label=False, show_download_button=False, show_fullscreen_button=False)
                    gr.Button("查看更多!!", link="/collage_gallery")
                with gr.Column():
                    gr.Image(
                        'static/worksheet_cover.jpg', elem_classes="gallery_cover",
                        container=False, show_label=False, show_download_button=False, show_fullscreen_button=False)
                    gr.Button("查看更多!!", link="/huge_poster_creation")

            gr.Button("體驗生成式人工智慧!!", link="/generative_ai")

    def mount(self, app, url):
        return gr.mount_gradio_app(app, self.index_page, path=url)
