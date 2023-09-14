"""Test Baidu Qianfan Chat Endpoint."""

from langchain.callbacks.manager import CallbackManager
from langchain.chat_models.baidu_qianfan_endpoint import QianfanChatEndpoint
from langchain.schema import (
    AIMessage,
    BaseMessage,
    ChatGeneration,
    HumanMessage,
    LLMResult,
)
from tests.unit_tests.callbacks.fake_callback_handler import FakeCallbackHandler


def test_default_call() -> None:
    """Test default model(`ERNIE-Bot`) call."""
    chat = QianfanChatEndpoint()
    response = chat(messages=[HumanMessage(content="Hello")])
    assert isinstance(response, BaseMessage)
    assert isinstance(response.content, str)


def test_model() -> None:
    """Test model kwarg works."""
    chat = QianfanChatEndpoint(model="BLOOMZ-7B")
    response = chat(messages=[HumanMessage(content="Hello")])
    assert isinstance(response, BaseMessage)
    assert isinstance(response.content, str)


def test_endpoint() -> None:
    """Test user custom model deployments like some open source models."""
    chat = QianfanChatEndpoint(endpoint="qianfan_bloomz_7b_compressed")
    response = chat(messages=[HumanMessage(content="Hello")])
    assert isinstance(response, BaseMessage)
    assert isinstance(response.content, str)


def test_multiple_history() -> None:
    """Tests multiple history works."""
    chat = QianfanChatEndpoint()

    response = chat(
        messages=[
            HumanMessage(content="Hello."),
            AIMessage(content="Hello!"),
            HumanMessage(content="How are you doing?"),
        ]
    )
    assert isinstance(response, BaseMessage)
    assert isinstance(response.content, str)


def test_stream() -> None:
    """Test that stream works."""
    chat = QianfanChatEndpoint(streaming=True)
    callback_handler = FakeCallbackHandler()
    callback_manager = CallbackManager([callback_handler])
    response = chat(
        messages=[
            HumanMessage(content="Hello."),
            AIMessage(content="Hello!"),
            HumanMessage(content="Who are you?"),
        ],
        stream=True,
        callbacks=callback_manager,
    )
    assert callback_handler.llm_streams > 0
    assert isinstance(response.content, str)


def test_multiple_messages() -> None:
    """Tests multiple messages works."""
    chat = QianfanChatEndpoint()
    message = HumanMessage(content="Hi, how are you.")
    response = chat.generate([[message], [message]])

    assert isinstance(response, LLMResult)
    assert len(response.generations) == 2
    for generations in response.generations:
        assert len(generations) == 1
        for generation in generations:
            assert isinstance(generation, ChatGeneration)
            assert isinstance(generation.text, str)
            assert generation.text == generation.message.content
