import requests

from config import GROQ_API_KEY


GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

MODEL_NAME = "openai/gpt-oss-20b"

MAX_CONTEXT_CHARS = 16000


def generate_answer(question: str, contexts: list[str]):

    context = "\n\n".join(contexts)

    # Limit the amount of retrieved context
    # sent to the LLM.
    context = context[:MAX_CONTEXT_CHARS]

    prompt = f"""
You are a helpful assistant that answers questions about web development.

Use the provided context to answer the user's question.

Do not invent information.

If the answer is not available in the context, say:
"I don't have enough information in the provided data."

Context:
{context}

Question:
{question}

Answer:
"""

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.2,
        "max_tokens": 700
    }

    response = requests.post(
        GROQ_URL,
        headers=headers,
        json=data
    )

    if response.status_code != 200:
        raise Exception(
            f"Groq API Error: {response.status_code} - {response.text}"
        )

    result = response.json()

    return result["choices"][0]["message"]["content"]