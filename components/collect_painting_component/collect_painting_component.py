from components.prompt_dict import prompt_dict
from components.collect_painting_component.printing import print_image
from pathlib import Path

import gradio as gr


class CollectPaintingComponent:
    def __init__(self, image_name, access_token):
        self.access_token = access_token
        self.image_path = list(Path('static').rglob(f'{image_name}*'))[0]

        with gr.Blocks() as self.page:
            with gr.Row():
                with gr.Column(scale=1):
                    gr.Image(self.image_path, label=self.image_path.stem, height='40vh')
                    gr.Textbox(label="Prompt", lines=10, value=prompt_dict[self.image_path.stem], show_copy_button=True)
                    print_btn = gr.Button("Print It!")

                with gr.Column(scale=2):
                    with gr.Row(equal_height=True):
                        with gr.Column(scale=1):
                            upload_image = gr.Image()
                        with gr.Column(scale=2):
                            name = gr.Textbox(label="Name")
                            id_ = gr.Textbox(label="ID", interactive=True)
                            save_btn = gr.Button("Save!")

                    user_history = gr.State([])

                    @gr.render(inputs=user_history)
                    def render_user_history(user_history):
                        for history in user_history:
                            with gr.Row(equal_height=True, max_height="30vh"):
                                with gr.Column(scale=1):
                                    gr.Image(history['url'])
                                with gr.Column(scale=2):
                                    gr.Textbox(label="Name", value=history['name'])

            image_state = gr.State(None)

            print_btn.click(self.print_image)
            save_btn.click(
                self.save_history,
                [upload_image, name, user_history, image_state],
                [upload_image, name, id_, user_history, image_state])

            image_state.change(self.update_image, image_state, upload_image)
            timer = gr.Timer(value=1)
            timer.tick(self.upload_image, None, image_state)

        self.page.queue()
        self.page.run_startup_events()

    def save_history(self, url, name, user_history, image_url):
        user_history.append({
            'url': url,
            'name': name,
        })

        Path(image_url).unlink()
        return None, "", "", user_history, None

    def upload_image(self):
        jpgs = list(Path('static/upload').glob('*.jpg'))
        return f"{jpgs[0]}" if len(jpgs) > 0 else None

    def update_image(self, image_path):
        return image_path

    def delete_image(self, image_path):
        Path(image_path).unlink()

    def print_image(self):
        print_image(self.image_path, self.access_token)

    def mount(self, app, url):
        return gr.mount_gradio_app(app, self.page, path=url)
