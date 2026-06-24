import google.generativeai as genai
from PIL import Image
import json

# 🔥 LANGSUNG TARUH API KEY DI SINI

model = genai.GenerativeModel("gemini-3.1-flash-lite")


def analyze_food(image_file):

    image = Image.open(image_file)

    prompt = """
    Analisis gambar makanan ini.

    Balas HANYA dalam format JSON berikut:

    {
        "food": "nama makanan",
        "calories": 0,
        "protein": 0,
        "fat": 0,
        "carbohydrate": 0,
        "analysis": "analisis singkat"
    }

    Estimasikan nilai nutrisi secara realistis.
    """

    response = model.generate_content([prompt, image])

    text = response.text.strip()

    text = text.replace("```json", "").replace("```", "")

    return json.loads(text)