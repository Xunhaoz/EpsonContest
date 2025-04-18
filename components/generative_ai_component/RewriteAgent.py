import json
import base64

from openai import OpenAI


class RewriteAgent:
    system_prompt = """You are a powerful AI that can rewrite good prompt for image generation based on user input.

When rewriting prompts, consider the following guidelines:
* **Be Specific and Detailed**: The more specific your prompt, the better the image quality. Include details like the setting, objects, colors, mood, and any specific elements you want in the image.
* **Mood and Atmosphere**: Describe the mood or atmosphere you want to convey. Words like “serene,” “chaotic,” “mystical,” or “futuristic” can guide the AI in setting the right tone.
* **Use Descriptive Adjectives**: Adjectives help in refining the image. For example, instead of saying “a dog,” say “a fluffy, small, brown dog.”
* **Consider Perspective and Composition**: Mention if you want a close-up, a wide shot, a bird’s-eye view, or a specific angle. This helps in framing the scene correctly.
* **Specify Lighting and Time of Day**: Lighting can dramatically change the mood of an image. Specify if it’s day or night, sunny or cloudy, or if there’s a specific light source like candlelight or neon lights.
* **Incorporate Action or Movement**: If you want a dynamic image, describe actions or movements. For instance, “a cat jumping over a fence” is more dynamic than just “a cat.”
* **Avoid Overloading the Prompt**: While details are good, too many can confuse the AI. Try to strike a balance between being descriptive and being concise.
* **Use Analogies or Comparisons**: Sometimes it helps to compare what you want with something well-known, like “in the style of Van Gogh” or “resembling a scene from a fantasy novel.”
* **Specify Desired Styles or Themes**: If you have a particular artistic style or theme in mind, mention it. For example, “cyberpunk,” “art deco,” or “minimalist.”
"""

    user_prompt = """The following is a user input that rewrites prompts for image generation. The AI is designed to help users create more effective and detailed prompts for generating images.

<USER_INPUT>
{user_input}
</USER_INPUT>
"""

    user_prompt_image = """According to the user input and the uploaded image, rewrite the prompt for image generation. The AI is designed to help users create more effective and detailed prompts for generating images.

<USER_INPUT>
{user_input}
</USER_INPUT>
"""

    def __init__(self, api_key=None):
        self.client = OpenAI(api_key=api_key)

    def encode_image(self, image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")

    def prompt_call(self, user_input):
        response = self.client.responses.create(
            model="o4-mini",
            input=[
                {'role': 'system', 'content': self.system_prompt},
                {"role": "user", "content": self.user_prompt.format(user_input=user_input)}
            ],
            text={
                "format": {
                    "type": "json_schema",
                    "name": "prompt",
                    "schema": {
                        "type": "object",
                        "properties": {
                            "prompt": {"type": "string"}
                        },
                        "required": ["prompt"],
                        "additionalProperties": False
                    },
                    "strict": True
                },
            },
        )
        return json.loads(response.output_text)['prompt']

    def prompt_image_call(self, user_input, file):
        response = self.client.responses.create(
            model="o4-mini",
            input=[
                {'role': 'system', 'content': self.system_prompt},
                {"role": "user", "content": [
                    {"type": "input_text", "text": self.user_prompt_image.format(user_input=user_input)},
                    {
                        "type": "input_image",
                        "image_url": f"data:image/jpeg;base64,{self.encode_image(file)}",
                    }
                ]}
            ],
            text={
                "format": {
                    "type": "json_schema",
                    "name": "prompt",
                    "schema": {
                        "type": "object",
                        "properties": {
                            "prompt": {"type": "string"}
                        },
                        "required": ["prompt"],
                        "additionalProperties": False
                    },
                    "strict": True
                },
            },
        )
        return json.loads(response.output_text)['prompt']
