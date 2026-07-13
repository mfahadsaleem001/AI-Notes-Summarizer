from google import genai
from models.config import GEMINI_API_KEY


client = genai.Client(api_key=GEMINI_API_KEY)

def summarize_text(text, summary_mode):

    if summary_mode == "short":

        instruction = """
Create a SHORT summary.

Rules:
- Maximum 5-8 numbered points.
- Keep each point concise.
- Focus only on the most important ideas.
"""

    elif summary_mode == "medium":

        instruction = """
Create a MEDIUM summary.

Rules:
- Include a brief introduction.
- Add 8-12 numbered key points.
- Finish with a short conclusion.
"""

    elif summary_mode == "detailed":

        instruction = """
Create a DETAILED summary.

Rules:
- Explain every important topic.
- Use headings.
- Use numbered points.
- Add a proper conclusion.
"""

    elif summary_mode == "exam":

        instruction = """
Create an EXAM REVISION SHEET.

Include these sections:

1. Important Topics

2. Important Definitions

3. Key Concepts

4. Quick Revision Notes

5. Exam Tips

Use proper headings and numbered lists.
"""

    else:

        instruction = """
Create a medium summary with numbered points.
"""

    prompt = f"""
You are Smart Study AI.

Your task is to summarize university lecture notes professionally.

Formatting Rules:

- Do NOT use Markdown symbols (*, **, #).
- Write headings in CAPITAL LETTERS.
- Leave exactly ONE blank line after every heading.
- Do NOT leave blank lines between numbered points.
- Use numbered lists only.
- Make the summary look like a professional report.
- Keep the language simple and easy to study.

Example Format:

INTRODUCTION
This is the introduction.

KEY POINTS
1. First point.
2. Second point.
3. Third point.

CONCLUSION
This is the conclusion.

{instruction}

Lecture Notes:

{text}
"""

    prompt = prompt.encode("utf-8", "ignore").decode("utf-8")

    response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents=prompt
    )

    return response.text