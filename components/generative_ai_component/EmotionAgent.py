import json
import base64

from openai import OpenAI


class EmotionAgent:
    system_prompt = """You are a kind agent that can compliment the user based on their input."""

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
                {"role": 'user', 'content': user_input}
            ],
            text={
                "format": {
                    "type": "json_schema",
                    "name": "emotion",
                    "schema": {
                        "type": "object",
                        "properties": {
                            "compliment": {"type": "string"}
                        },
                        "required": ["compliment"],
                        "additionalProperties": False
                    },
                    "strict": True
                },
            },
        )
        return json.loads(response.output_text)['compliment']

    def prompt_image_call(self, user_input, file):
        response = self.client.responses.create(
            model="o4-mini",
            input=[
                {'role': 'system', 'content': self.system_prompt},
                {"role": 'user', 'content': [
                    {"type": "input_text", "text": user_input},
                    {
                        "type": "input_image",
                        "image_url": f"data:image/jpeg;base64,{self.encode_image(file)}",
                    }
                ]}
            ],
            text={
                "format": {
                    "type": "json_schema",
                    "name": "emotion",
                    "schema": {
                        "type": "object",
                        "properties": {
                            "compliment": {"type": "string"}
                        },
                        "required": ["compliment"],
                        "additionalProperties": False
                    },
                    "strict": True
                },
            },
        )
        return json.loads(response.output_text)['compliment']
