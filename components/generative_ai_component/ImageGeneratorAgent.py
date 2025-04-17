import requests
from io import BytesIO
import imageio

from openai import OpenAI


class ImageGeneratorAgent:
    def __init__(self, api_key=None):
        self.client = OpenAI(api_key=api_key)

    def call(self, prompt):
        response = self.client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1792x1024",
            quality="standard",
            n=1,
        )
        res = requests.get(response.data[0].url)
        img_arr = imageio.imread(BytesIO(res.content))
        return img_arr
