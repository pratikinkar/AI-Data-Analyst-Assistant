
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

def get_groq_client():
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError(
            "GROQ_API_KEY missing. Check your .env file."
        )

    return Groq(api_key=api_key)


def generate_ai_response(messages):
    client = get_groq_client()

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=messages,
        temperature=0.2,
        max_tokens=1000
    )

    return response.choices[0].message.content

