import pytest
from chatgptonic.integration import ChatGPT


@pytest.fixture()
def chatgpt():
    return ChatGPT("some_api_key")
