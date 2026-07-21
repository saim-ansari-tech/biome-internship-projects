import os
from groq import Groq
from dotenv import load_dotenv


load_dotenv()

api_key = os.getenv("GROQ_API_KEY")


if not api_key:
    raise ValueError(
        "GROQ_API_KEY not found in environment variables."
    )


client = Groq(
    api_key=api_key
)


def generate_answer(
    question: str,
    context: str
):

    prompt = f"""You are an AI assistant that
answers questions about an uploaded video.

Your task is to answer the user's question using
the information contained in the provided video context.

RULES:
1. If the context contains relevant information,
answer the question using that information.
2. If the context is partially relevant,
provide what information is available and note what is not covered.
3. Only say "Sorry, I cannot find this information in the video"
if the context is completely unrelated to the question.
4. Be helpful and informative. Use the context to provide a detailed answer.
5. If the user asks about the video's content,
summary, or main topics, use the transcript context to answer.

Video Context:
{context}

User Question:
{question}

Answer:
"""

    response = client.chat.completions.create(

        model="llama-3.1-8b-instant",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0.3,

    )

    return response.choices[0].message.content
