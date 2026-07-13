from google import genai
from models.config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)


def generate_quiz(text, total_questions=5):

    prompt = f"""
You are an AI Quiz Generator.

Read the following notes carefully and generate:

1. Generate {total_questions} Multiple Choice Questions (MCQs).
2. Each MCQ should have four options:
   A)
   B)
   C)
   D)
3. Mention the correct answer after every question.
4. Keep questions exam-focused.

Use this format:

Q1: Question

A) Option
B) Option
C) Option
D) Option

Correct Answer: Option

Notes:

{text}
"""

    prompt = prompt.encode("utf-8", "ignore").decode("utf-8")

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt
    )

    return response.text