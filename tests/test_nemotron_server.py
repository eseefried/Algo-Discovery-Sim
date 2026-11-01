from fastapi.testclient import TestClient

from algo_discovery.nemotron_server import create_app


class FakeModel:
    def generate(self, request, schema):
        assert schema == {"type": "object"}
        return {"model": request.model, "choices": [],
                "usage": {"prompt_tokens": 4, "completion_tokens": 2}}


def test_server_lists_shared_model_and_routes_schema():
    client = TestClient(create_app(FakeModel()))
    assert client.get("/v1/models").json()["data"][0]["id"] == "nemotron-quantum"
    body = {"model": "nemotron-quantum", "messages": [{"role": "user", "content": "hi"}],
            "response_format": {"type": "json_schema", "json_schema": {"schema": {"type": "object"}}}}
    assert client.post("/v1/chat/completions", json=body).json()["usage"]["prompt_tokens"] == 4
    assert client.post("/v1/chat/completions", json=body | {"model": "wrong"}).status_code == 404
    assert client.post("/v1/chat/completions", json=body | {"response_format": {}}).status_code == 400


def test_base_alias_disables_lora_and_caller_cannot_override_mapping():
    class Probe:
        def generate(self, request, schema):
            return {"adapter": request.use_adapter}

    client = TestClient(create_app(Probe(), serve_base=True))
    body = {"model": "nemotron-quantum-base", "messages": [{"role": "user", "content": "hi"}],
            "response_format": {"type": "json_schema", "json_schema": {"schema": {}}},
            "use_adapter": True}
    assert client.post("/v1/chat/completions", json=body).json() == {"adapter": False}
    assert client.post("/v1/chat/completions", json=body | {
        "model": "nemotron-quantum", "use_adapter": False}).json() == {"adapter": True}
    assert len(client.get("/v1/models").json()["data"]) == 2


def test_plain_text_preserves_training_messages_without_schema():
    class TextProbe:
        def generate(self, request, schema):
            assert schema is None
            assert request.messages[0].content == "Output only numbered LaTeX equations."
            return {"choices": [{"message": {"content": "(1) H\\psi\n<END_EQUATIONS>"}}]}

    client = TestClient(create_app(TextProbe()))
    body = {"model": "nemotron-quantum", "messages": [
        {"role": "system", "content": "Output only numbered LaTeX equations."},
        {"role": "user", "content": "Abstract: test\n\nStart equation: 1"}]}
    for fmt in [None, {"type": "text"}]:
        assert client.post("/v1/chat/completions", json=body | {"response_format": fmt}).status_code == 200
