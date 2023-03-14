import pytest
from unittest.mock import patch

from chatgptonic.integration import ChatGPTMessageException, ChatGPT


class TestChatGPTMessageException:
    def test_parent_class(self):
        assert issubclass(ChatGPTMessageException, Exception)


class TestChatGPT:
    def test_init_without_optional_fields(self, chatgpt):
        assert chatgpt.api_key == "some_api_key"
        assert chatgpt.chat_model == "gpt-3.5-turbo"
        assert chatgpt.role == "user"

    def test_init_with_optional_fields(self):
        chat = ChatGPT("some_api_key", "some_chat_model", "some_role")

        assert chat.api_key == "some_api_key"
        assert chat.chat_model == "some_chat_model"
        assert chat.role == "some_role"

    def test_get_headers(self, chatgpt):
        headers = chatgpt._get_headers()

        assert headers == {
            "Content-Type": "application/json",
            "Authorization": f"Bearer some_api_key"
        }

    def test_get_body(self, chatgpt):
        body = chatgpt._get_body("some_message", creativity=.8)

        assert body == {
            "model": chatgpt.chat_model,
            "messages": [{"role": chatgpt.role, "content": "some_message"}],
            "temperature": .8
        }

    @patch("chatgptonic.integration.json")
    @patch.object(ChatGPT, "_get_body")
    @patch.object(ChatGPT, "_get_headers")
    def test_get_request(
        self, mock_get_headers, mock_get_body, mock_json, chatgpt
    ):
        request = chatgpt._get_request("some_message", creativity=.9)
        mock_get_body.assert_called_once_with("some_message", .9)
        mock_get_headers.assert_called_once()
        mock_json.dumps.assert_called_once_with(
            mock_get_body.return_value
        )

        assert request == {
            "url": chatgpt.chat_url,
            "data": mock_json.dumps.return_value,
            "headers": mock_get_headers.return_value
        }

    @patch("chatgptonic.integration.json")
    @patch("chatgptonic.integration.requests")
    @patch.object(ChatGPT, "_get_request", return_value={"url": "some_url"})
    def test_send_successfully(
        self, mock_get_request, mock_requests, mock_json, chatgpt
    ):
        mock_requests.post.return_value.status_code = 200
        response = chatgpt.send("some_message", creativity=1)

        mock_get_request.assert_called_once_with("some_message", 1)
        mock_requests.post.assert_called_once_with(url="some_url")

        mock_json.loads.assert_called_once_with(mock_requests.post.return_value.content)

        assert response == mock_json.loads.return_value

    @patch("chatgptonic.integration.json")
    @patch("chatgptonic.integration.requests")
    @patch.object(ChatGPT, "_get_request", return_value={"url": "some_url"})
    def test_send_failure(
        self, mock_get_request, mock_requests, mock_json, chatgpt
    ):
        mock_requests.post.return_value.status_code = 400
        mock_json.loads.return_value = {"error": {"message": "some_error_message"}}

        with pytest.raises(ChatGPTMessageException) as error:
            chatgpt.send("some_message", creativity=1)

        mock_get_request.assert_called_once_with("some_message", 1)
        mock_requests.post.assert_called_once_with(url="some_url")

        mock_json.loads.assert_called_once_with(mock_requests.post.return_value.content)

        assert str(error.value) == (
            "Something went wrong with this error message: some_error_message"
        )

    @patch.object(
        ChatGPT,
        "send",
        return_value={"choices": [{"message": {"content": "\n\nsome_response"}}]}
    )
    def test_just_chat(self, mock_send, chatgpt):
        response = chatgpt.just_chat("some_message", creativity=.4)
        mock_send.assert_called_once_with("some_message", creativity=.4)

        assert response == "some_response"

    @patch.object(ChatGPT, "just_chat", return_value="some_gpt_message")
    @patch("chatgptonic.integration.input")
    @patch("chatgptonic.integration.print")
    def test_interactive_chat_with_quit_input(
        self, mock_print, mock_input, mock_just_chat, chatgpt
    ):
        mock_input.return_value = "c"
        chatgpt.start_interactive_chat()
        mock_input.assert_called_once_with(f"\033[92m [0.] You: \033[0m")
        mock_just_chat.assert_not_called()
        mock_print.assert_not_called()
