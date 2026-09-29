"""Exercise the isolated OpenAI provider without sending a network request."""

import inspect
import json

import httpx
import pytest
from openai import OpenAI as SDKOpenAI
from openai import AuthenticationError, OpenAIError

import app
from product_data_copilot.ai import provider


def test_provider_configuration_is_isolated_from_app():
    app_source = inspect.getsource(app)
    assert "from openai import" not in app_source
    assert "OPENAI_API_KEY" not in app_source
    assert "OPENAI_MODEL" not in app_source
    assert "timeout=45.0" not in app_source
    assert "max_retries=1" not in app_source
    assert app.request_content_draft is provider.request_content_draft
    assert app.has_openai_api_key is provider.has_openai_api_key


def test_content_request_uses_the_real_sdk_offline(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "offline-test-key")
    monkeypatch.setenv("OPENAI_MODEL", "test-model")
    requests = []
    response_text = json.dumps({"sku": "TEST", "de_html": "<p>Test</p>"})

    def handle(request):
        assert request.method == "POST"
        assert request.url.path == "/v1/responses"
        assert request.headers["authorization"] == "Bearer offline-test-key"
        requests.append(json.loads(request.content))
        return httpx.Response(200, json={
            "id": "resp_offline_test",
            "object": "response",
            "created_at": 0,
            "model": "test-model",
            "status": "completed",
            "output": [{
                "id": "msg_offline_test",
                "type": "message",
                "role": "assistant",
                "status": "completed",
                "content": [{"type": "output_text", "text": response_text, "annotations": []}],
            }],
        })

    clients = []

    def offline_client(**options):
        assert options == {
            "api_key": "offline-test-key",
            "timeout": 45.0,
            "max_retries": 1,
        }
        client = SDKOpenAI(
            **options,
            http_client=httpx.Client(transport=httpx.MockTransport(handle)),
        )
        clients.append(client)
        return client

    monkeypatch.setattr(provider, "OpenAI", offline_client)
    try:
        result = provider.request_content_draft("Only this fictional product")
    finally:
        for client in clients:
            client.close()

    assert result == response_text
    assert requests == [{
        "model": "test-model",
        "input": "Only this fictional product",
        "max_output_tokens": 3000,
        "text": {"format": {"type": "json_object"}},
    }]


def test_missing_api_key_fails_before_any_request(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    assert not provider.has_openai_api_key()
    with pytest.raises(OpenAIError, match="api_key"):
        provider.request_content_draft("No request may leave this test")


def test_invalid_api_key_fails_safely_with_offline_response(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "invalid-offline-key")
    requests = []

    def handle(request):
        requests.append(request)
        return httpx.Response(
            401,
            json={"error": {"message": "Invalid API key", "type": "invalid_request_error"}},
        )

    clients = []

    def offline_client(**options):
        client = SDKOpenAI(
            **options,
            http_client=httpx.Client(transport=httpx.MockTransport(handle)),
        )
        clients.append(client)
        return client

    monkeypatch.setattr(provider, "OpenAI", offline_client)
    try:
        with pytest.raises(AuthenticationError):
            provider.request_content_draft("Offline invalid-key test")
    finally:
        for client in clients:
            client.close()

    assert len(requests) == 1
