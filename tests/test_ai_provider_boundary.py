"""Exercise the installed OpenAI SDK without sending a network request."""

import json

import httpx
from openai import OpenAI as SDKOpenAI

import app


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
        client = SDKOpenAI(
            **options,
            http_client=httpx.Client(transport=httpx.MockTransport(handle)),
        )
        clients.append(client)
        return client

    monkeypatch.setattr(app, "OpenAI", offline_client)
    try:
        result = app.request_content_draft("Only this fictional product")
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
