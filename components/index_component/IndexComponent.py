import gradio as gr


class IndexComponent:
    def __init__(self):
        with gr.Blocks(fill_height=True) as self.index_page:
            gr.Markdown("# Epson Innovation Challenge 2025 創新大賽")
            gr.Image()

            with gr.Row():
                with gr.Column():
                    gr.Markdown("# 填色線稿畫廊")
                    gr.Image()
                    gr.Button("查看更多!!", link="/coloring_gallery")
                with gr.Column():
                    gr.Markdown("# 拼貼畫廊")
                    gr.Image()
                    gr.Button("查看更多!!", link="/collage_gallery")
                with gr.Column():
                    gr.Markdown("# 巨海製作器")
                    gr.Image(height="100%")
                    gr.Button("查看更多!!", link="/huge_poster_creation")

            gr.Button("體驗生成式人工智慧!!", link="/generative_ai")

    def mount(self, app, url):
        return gr.mount_gradio_app(app, self.index_page, path=url)
