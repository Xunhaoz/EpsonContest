from pathlib import Path
import time

from sqlalchemy.testing.suite.test_reflection import users

from components.generative_ai_component.RewriteAgent import RewriteAgent
from components.generative_ai_component.EmotionAgent import EmotionAgent
from components.generative_ai_component.ImageGeneratorAgent import ImageGeneratorAgent
from components.prompt_dict import prompt_dict, prompt_2_pic

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
        with gr.Blocks() as self.generative_ai_page:
            gr.Markdown("# Epson Innovation Challenge 2025 創新大賽")
            with gr.Row(equal_height=True):
                with gr.Column():
                    image = gr.Image(label="生成的圖片", interactive=False, show_download_button=True, height="80vh")
                with gr.Column():
                    chatbot = gr.Chatbot(elem_id="chatbot", type="messages", autoscroll=True, height="60vh")
                    chat_input = gr.MultimodalTextbox(
                        file_count="single",
                        placeholder="Enter message or upload file...",
                        show_label=False,
                        sources=["upload"],
                        file_types=[".jpg", ".png", ".jpeg"],
                        lines=2
                    )

                    image_state = gr.State([])

            chat_input.submit(
                self.input2prompt, [chatbot, chat_input], chatbot,
                show_progress_on=[image, chat_input]
            ).then(
                self.prompt2image, [chatbot], image,
                show_progress_on=[image, chat_input]
            )

            chat_input.change(self.delete_image, [chat_input, image_state], None)

            timer = gr.Timer(value=1)
            timer.tick(self.upload_image, None, image_state)

            image_state.change(self.update_image, [chat_input, image_state], chat_input)

    def delete_image(self, user_input, image_urls):
        if len(user_input['files']) < len(image_urls):
            Path(image_urls[0]).unlink()

    def upload_image(self):
        jpgs = list(Path('static/upload').glob('*.jpg'))
        return [f"{jpgs[0]}"] if len(jpgs) > 0 else []

    def update_image(self, user_input, image_urls):
        if image_urls:
            user_input['files'] = image_urls
        else:
            user_input['files'] = image_urls
        return user_input

    def input2prompt(self, history, user_input, progress=gr.Progress()):
        if len(user_input['files']) == 1 and user_input['text'] != "":
            yield from self.chat_image2prompt(history, user_input['text'], user_input['files'][0], progress)
        elif user_input['text'] != "":
            yield from self.chat2prompt(history, user_input['text'], progress)
        return history

    def chat_image2prompt(self, history, text, file, progress=gr.Progress()):
        progress.tqdm(None, total=4, desc="GAI understanding...", unit="step")

        history.append(ChatMessage(role="user", content={"path": file}))
        history.append(ChatMessage(role="user", content=text))
        history.append(ChatMessage(role="assistant", content='Got it! Let me see...'))
        yield history

        progress.update(1)
        compliment = EmotionAgent().prompt_image_call(text, file)
        history.append(ChatMessage(role="assistant", content=compliment, metadata={"title": "💡Thinking..."}))
        yield history

        progress.update(1)
        time.sleep(1)
        history.append(
            ChatMessage(role="assistant",
                        content='In order to generate a excellent image. Prompt Rewriting...✍️'))
        yield history

        progress.update(1)
        prompt = RewriteAgent().prompt_image_call(text, file)
        history.append(ChatMessage(
            role="assistant", content=prompt,
            metadata={"title": "I think this good prompt can help you generate a image.🫡"}))
        yield history

        progress.update(1)
        time.sleep(1)
        history.append(
            ChatMessage(role="assistant", content='Generating image....️'))
        yield history

    def chat2prompt(self, history, text, progress=gr.Progress()):
        progress.tqdm(None, total=4, desc="GAI understanding...", unit="step")

        history.append(ChatMessage(role="user", content=text))
        history.append(ChatMessage(role="assistant", content='Got it! Let me see...'))
        yield history

        progress.update(1)
        compliment = EmotionAgent().prompt_call(text)
        history.append(ChatMessage(role="assistant", content=compliment, metadata={"title": "💡Thinking..."}))
        yield history

        progress.update(1)
        time.sleep(1)
        history.append(
            ChatMessage(role="assistant",
                        content='In order to generate a excellent image. Prompt Rewriting...✍️'))
        yield history

        progress.update(1)
        prompt = RewriteAgent().prompt_call(text)
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
        prompt = history[-2]['content']
        users_prompt = history[-6]['content']

        if users_prompt in prompt_2_pic:
            return list(Path('static').rglob(f'{prompt_2_pic[users_prompt]}*'))[0]

        if 'baby penguin' in prompt:
            return 'static/ghibli_practice_word/penguin_ghibli_practice_word.png'

        if 'sea otter' in prompt:
            return 'static/ghibli_practice_word/sea_otter_ghibli_practice_word.png'

        if 'baby wombat ' in prompt:
            return 'static/ghibli_practice_word/wombat_ghibli_practice_word.png'

        ndarr = ImageGeneratorAgent().call(prompt)
        return ndarr

    def mount(self, app, url):
        return gr.mount_gradio_app(app, self.generative_ai_page, path=url)
