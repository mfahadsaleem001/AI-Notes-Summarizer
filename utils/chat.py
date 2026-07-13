import google.generativeai as genai

from models.config import GEMINI_API_KEY

from utils.embeddings import get_embedding_model
from utils.rag import rag_db

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")


def ask_question(question):

    embedding_model = get_embedding_model()

    question_embedding = embedding_model.encode(
        question,
        convert_to_numpy=True
    )

    relevant_chunks = rag_db.search(
        question_embedding,
        top_k=3
    )

    context = "\n\n".join(relevant_chunks)

    prompt = f"""
You are an AI Notes Assistant.

Answer ONLY using the information provided below.

If the answer is not available in the uploaded notes, reply exactly:

"I couldn't find the answer in the uploaded notes."

-------------------------
NOTES
-------------------------

{context}

-------------------------
QUESTION
-------------------------

{question}

Rules:

1. Answer in simple English.
2. Do not make up information.
3. Keep the answer clear and concise.
4. Use only the uploaded notes.
"""

    response = model.generate_content(prompt)

    return response.text.strip()