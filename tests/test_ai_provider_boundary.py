"""Exercise the installed OpenAI SDK without sending a network request."""

import json

import httpx
import pandas as pd
from openai import OpenAI as SDKOpenAI

import app


def test_configured_key_and_v2_response_use_the_real_sdk_offline(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "offline-test-key")
    monkeypatch.setenv("OPENAI_MODEL", "test-model")
    requests = []
    response_text = json.dumps({"smart_suggestions": []})

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
        result = app.generate_smart_suggestions_v2("Only this fictional product")
    finally:
        for client in clients:
            client.close()

    assert result == response_text
    assert requests == [{
        "model": "test-model",
        "input": "Only this fictional product",
        "max_output_tokens": 3000,
    }]


def test_classic_ai_parses_sdk_response_offline(valid_product, monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "offline-test-key")
    monkeypatch.delenv("OPENAI_MODEL", raising=False)
    requests = []

    def handle(request):
        assert request.method == "POST"
        assert request.url.path == "/v1/responses"
        assert request.headers["authorization"] == "Bearer offline-test-key"
        requests.append(json.loads(request.content))
        return httpx.Response(200, json={
            "id": "resp_offline_classic",
            "object": "response",
            "created_at": 0,
            "model": "gpt-4.1-mini",
            "status": "completed",
            "output": [{
                "id": "msg_offline_classic",
                "type": "message",
                "role": "assistant",
                "status": "completed",
                "content": [{"type": "output_text", "text": '{"improved_product_title":"Office Box"}', "annotations": []}],
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
        result = app.generate_ai_suggestions(
            pd.Series(valid_product), pd.DataFrame(),
            pd.Series({"sku": valid_product["sku"], "overall_readiness_score": 80}),
            ["Improved Product Title"],
        )
    finally:
        for client in clients:
            client.close()

    assert result["improved_product_title"] == "Office Box"
    assert requests[0]["model"] == "gpt-4.1-mini"
    assert "000123" in requests[0]["input"]
