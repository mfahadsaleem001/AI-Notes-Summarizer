from google import genai
from models.config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)


def generate_viva(text):

    prompt = f"""
You are an experienced university viva examiner.

Read the following notes carefully and generate viva preparation questions.

Rules:

1. Generate exactly 10 viva questions.
2. After every question, provide a short and accurate expected answer.
3. Questions should be practical and commonly asked in university vivas.
4. Keep answers simple, professional, and easy to remember.
5. Use the following format:

Viva 1

Question:
...

Expected Answer:
...

Viva 2

Question:
...

Expected Answer:
...

Notes:

{text}
"""

    prompt = prompt.encode("utf-8", "ignore").decode("utf-8")

    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents=prompt
    )

    return response.text