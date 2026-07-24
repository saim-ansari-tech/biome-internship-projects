import os
from dotenv import load_dotenv
from google import genai


load_dotenv()

api_key = os.getenv(
    "GEMINI_API_KEY"
)

client = genai.Client(
    api_key=api_key
)


def generate_answer(
    query,
    retrieved_documents
):

    context = "\n\n".join(

        document.page_content

        for document, score
        in retrieved_documents

    )

    prompt = f"""
You are a helpful document question-answering assistant.

Answer the user's question using ONLY the
information provided in the context.

If the answer cannot be found in the context,
say:

"I could not find the answer in the provided documents."

Do not make up information.
Do not use outside knowledge.

Context:
{context}

Question:
{query}

Answer:
"""
    response = client.models.generate_content(

        model="gemini-2.5-flash",

        contents=prompt

    )

    return response.text
