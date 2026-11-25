from dotenv import load_dotenv
from openai import OpenAI

import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv(
        "OPENAI_API_KEY"
    )
)


class IAService:

    @staticmethod
    def responder(
        pergunta
    ):

        resposta = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": pergunta
                }
            ]
        )

        return (
            resposta
            .choices[0]
            .message.content
        )