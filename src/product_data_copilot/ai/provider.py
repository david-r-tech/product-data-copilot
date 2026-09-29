"""OpenAI provider boundary for product-content requests."""

import os

from openai import OpenAI


def has_openai_api_key():
    """Return whether the provider API key is configured."""
    return bool(os.getenv("OPENAI_API_KEY"))


def request_content_draft(prompt):
    """Make one paid, JSON-constrained request for one product."""
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), timeout=45.0, max_retries=1)
    response = client.responses.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
        input=prompt,
        max_output_tokens=3000,
        text={"format": {"type": "json_object"}},
    )
    return response.output_text.strip()
