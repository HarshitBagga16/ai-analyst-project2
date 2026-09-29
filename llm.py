import os
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()
api_key = os.getenv("open_api_key") 


client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=api_key
)


def ask_llm(question, analysis_results):

    prompt = f"""
You are a data analyst assistant.

The following information was calculated by Python/Pandas
from a sales dataset.

Use ONLY these calculated results when answering the question.

Do not invent numbers.

Calculated results:
{analysis_results}

User question:
{question}

Give a clear and concise business-oriented answer.

If the available data is insufficient to answer the question,
say so.
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful and accurate data analyst."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content