from google import genai
from models.config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)


def generate_flashcards(text):

    prompt = f"""
You are an AI Flashcard Generator.

Read the following notes carefully and create useful study flashcards.

Rules:

1. Generate 10 flashcards.
2. Each flashcard must contain:
   - Question
   - Answer
3. Questions should be exam-focused.
4. Answers should be short and easy to remember.
5. Use this format:

Flashcard 1

Q:
Question here

A:
Answer here


Flashcard 2

Q:
Question here

A:
Answer here


Notes:

{text}
"""

    prompt = prompt.encode("utf-8", "ignore").decode("utf-8")

    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents=prompt
    )

    return response.text