import openai
import base64
import os
from dotenv import load_dotenv

load_dotenv()

# Ensure the environment variable is set
api_key = os.getenv("OPENAI_API_KEY")

# If it's not set, you'll need to raise an error
if not api_key:
    raise ValueError("The OPENAI_API_KEY environment variable is not set")

# Initialize the OpenAI client
openai.api_key = api_key

def create_from_data(data, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    image_number = 0
    for element in data:
        if element["type"] != "image":
            continue
        image_number += 1
        image_name = f"image_{image_number}.webp"
        generate(element["description"] + ". Vertical image, fully filling the canvas.", os.path.join(output_dir, image_name))

def generate(prompt, output_file, size="1024x1792"):
    response = openai.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size=size,
        quality="standard",
        response_format="b64_json",
        n=1,
    )

    image_b64 = response.data[0].b64_json

    with open(output_file, "wb") as f:
        f.write(base64.b64decode(image_b64))

