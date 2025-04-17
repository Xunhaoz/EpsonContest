import time

from components.generative_ai_component.RewriteAgent import RewriteAgent
from components.generative_ai_component.EmotionAgent import EmotionAgent
from components.generative_ai_component.ImageGeneratorAgent import ImageGeneratorAgent

import gradio as gr
from gradio import ChatMessage


class GenerativeAiComponent:
    head = """
    <style>
    textarea {
        font-size: 25px !important;
    }
    </style>
    """

    def __init__(self):
        with gr.Blocks(head=self.head) as self.generative_ai_page:
            with gr.Row():
                with gr.Column():
                    image = gr.Image(label="生成的圖片", interactive=False, height='1000px', show_download_button=True)
                with gr.Column():
                    with gr.Row(height='850px'):
                        chatbot = gr.Chatbot(type="messages", height='850px')
                    with gr.Row(height='70px'):
                        textbox = gr.Textbox(
                            container=False, placeholder='Hi there! How can I help you?', elem_id='input_textbox')
                    with gr.Row(height='50px'):
                        upload_image = gr.UploadButton("UPLOAD IMAGE", file_types=["image"])
                        submit = gr.Button("SUBMIT")

            submit.click(
                self.chat2prompt, [chatbot, textbox], chatbot,
                show_progress_on=[image, submit, upload_image, textbox]
            ).then(
                self.prompt2image, [chatbot], image,
                show_progress_on=[image, submit, upload_image, textbox]
            )

    def chat2prompt(self, history, user_input, progress=gr.Progress()):
        if user_input == "":
            return history, ""

        progress.tqdm(None, total=4, desc="GAI understanding...", unit="step")

        history.append(ChatMessage(role="user", content=user_input))
        yield history

        history.append(ChatMessage(role="assistant", content='Got it! Let me see...'))
        yield history

        progress.update(1)
        compliment = EmotionAgent().call(user_input)
        history.append(ChatMessage(role="assistant", content=compliment, metadata={"title": "💡Thinking..."}))
        yield history


        progress.update(1)
        time.sleep(1)
        history.append(
            ChatMessage(role="assistant", content='In order to generate a excellent image. Prompt Rewriting...✍️'))
        yield history

        progress.update(1)
        prompt = RewriteAgent().call(user_input)
        history.append(ChatMessage(
            role="assistant", content=prompt,
            metadata={"title": "I think this good prompt can help you generate a image.🫡"}))
        yield history

        progress.update(1)
        time.sleep(1)
        history.append(
            ChatMessage(role="assistant", content='Generating image....️'))
        yield history

    def prompt2image(self, history):
        ndarr = ImageGeneratorAgent().call(history[-2]['content'])
        return ndarr

    def mount(self, app, url):
        return gr.mount_gradio_app(app, self.generative_ai_page, path=url)
