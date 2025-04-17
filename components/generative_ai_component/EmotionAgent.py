import json

from openai import OpenAI


class EmotionAgent:
    system_prompt = """You are a kind agent that can compliment the user based on their input."""

    def __init__(self, api_key=None):
        self.client = OpenAI(api_key=api_key)

    def call(self, user_input):
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
