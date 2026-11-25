import ollama


class IALocalService:

    @staticmethod
    def responder(
        pergunta
    ):

        resposta = ollama.chat(
            model="llama3",
            messages=[
                {
                    "role": "user",
                    "content": pergunta
                }
            ]
        )

        return resposta[
            "message"
        ][
            "content"
        ]