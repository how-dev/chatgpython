import json

import requests


class ChatGPTMessageException(Exception):
    pass


class ChatGPT:
    def __init__(
        self,
        api_key: str,
        chat_model: str = "gpt-3.5-turbo",
        role: str = "user"
    ):
        self.api_key: str = api_key

        self.chat_model: str = chat_model
        self.role: str = role
        self.chat_url: str = (
            "https://api.openai.com/v1/chat/completions"
        )

    def _get_headers(self) -> dict:
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

    def _get_body(self, message: str, creativity: float) -> dict:
        return {
            "model": self.chat_model,
            "messages": [{"role": self.role, "content": message}],
            "temperature": creativity
        }

    def _get_request(self, message: str, creativity: float):
        body = self._get_body(message, creativity)
        headers = self._get_headers()

        return {
            "url": self.chat_url,
            "data": json.dumps(body),
            "headers": headers
        }

    def send(
        self,
        message: str,
        creativity: float = .7
    ) -> dict:
        request = self._get_request(message, creativity)

        response = requests.post(**request)
        response_json = json.loads(response.content)

        if response.status_code == 200:
            return response_json
        else:
            errors = response_json["error"]["message"]

        raise ChatGPTMessageException(
            f"Something went wrong with this error message: {errors}"
        )

    def just_chat(
        self,
        message: str,
        creativity: float = .7
    ) -> str:
        response = self.send(message, creativity=creativity)

        return response["choices"][0]["message"]["content"].replace("\n", "")
