import anthropic
import httpx
import pytest
from fastapi.testclient import TestClient

from src import api


@pytest.fixture
def client(monkeypatch):
    calls = []

    def fake_answer(query, k):
        calls.append((query, k))
        return {"answer": f"respuesta a {query}", "sources": ["MÓDULO 2 › EC2"]}

    monkeypatch.setattr(api, "answer", fake_answer)
    test_client = TestClient(api.app)
    test_client.calls = calls
    return test_client


def test_ask_returns_answer_and_sources(client):
    response = client.get("/ask", params={"query": "  ¿qué es EC2?  ", "k": 6})

    assert response.status_code == 200
    assert response.json() == {"answer": "respuesta a ¿qué es EC2?", "sources": ["MÓDULO 2 › EC2"]}
    # La query llega recortada y con el k pedido
    assert client.calls == [("¿qué es EC2?", 6)]


def test_ask_default_k_is_4(client):
    client.get("/ask", params={"query": "EC2"})
    assert client.calls == [("EC2", 4)]


@pytest.mark.parametrize("params", [{}, {"query": ""}, {"query": "   "}])
def test_ask_empty_query_returns_400(client, params):
    response = client.get("/ask", params=params)

    assert response.status_code == 400
    assert client.calls == []


@pytest.mark.parametrize("k", [0, 11])
def test_ask_k_out_of_range_returns_422(client, k):
    response = client.get("/ask", params={"query": "EC2", "k": k})
    assert response.status_code == 422


def test_ask_claude_error_returns_502(monkeypatch):
    def failing_answer(query, k):
        request = httpx.Request("POST", "https://api.anthropic.com/v1/messages")
        raise anthropic.APIConnectionError(request=request)

    monkeypatch.setattr(api, "answer", failing_answer)
    response = TestClient(api.app).get("/ask", params={"query": "EC2"})

    assert response.status_code == 502
    assert "Claude" in response.json()["detail"]
