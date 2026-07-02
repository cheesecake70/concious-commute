import os
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from google.genai.errors import APIError

# Mock GEMINI_API_KEY to bypass verify_gemini_api_key in tests
os.environ["GEMINI_API_KEY"] = "test_api_key"

from backend.main import app
client = TestClient(app)

async def mock_run_async_429(*args, **kwargs):
    raise APIError(code=429, response_json={"error": {"code": 429, "message": "Resource exhausted"}})
    yield

def test_get_syllabi():
    response = client.get("/api/syllabi")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 10
    assert "Engineering Mathematics III" in data
    assert "Human Resource Management" in data

@patch("google.adk.runners.InMemoryRunner.run_async", mock_run_async_429)
def test_get_modules_success():
    # Test valid subject matching and alias resolution
    response = client.get("/api/modules?subject=maths")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert "Module 1: Laplace Transform" in data

    response = client.get("/api/modules?subject=hrm")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert "Module 1: HRM Foundations and Strategic HRM" in data

def test_get_modules_invalid():
    # Test unsupported subject
    response = client.get("/api/modules?subject=InvalidSubject")
    assert response.status_code == 400
    assert "not supported" in response.json()["detail"]

@patch("google.adk.runners.InMemoryRunner.run_async", mock_run_async_429)
def test_generate_plan_mock_fallback():
    # Since we are using a test API key, agent execution will fail/fallback to mock
    # We test that the mock generator returns correct subject matching and does not fall back to Data Structures
    payload = {
        "source": "Churchgate",
        "destination": "Mumbai Central",
        "subject": "maths",
        "module": "any module",
        "is_peak": False
    }
    response = client.post("/api/generate", json=payload)
    assert response.status_code == 200
    data = response.json()
    
    assert data["source"] == "Churchgate"
    assert data["destination"] == "Mumbai Central"
    assert data["subject"] == "maths"
    assert data["is_too_short"] is False
    
    # Verify that mock plan actually contains Laplace Transform (Mathematics) and not Linked Lists (Data Structures)
    assert "Laplace" in data["study_plan"]
    assert "Linked List" not in data["study_plan"]

@patch("google.adk.runners.InMemoryRunner.run_async", mock_run_async_429)
def test_generate_plan_mock_fallback_hrm():
    payload = {
        "source": "Churchgate",
        "destination": "Mumbai Central",
        "subject": "Human Resource Management",
        "module": "any module",
        "is_peak": False
    }
    response = client.post("/api/generate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "HRM" in data["study_plan"]
    assert "Linked List" not in data["study_plan"]

def test_generate_plan_too_short():
    # Churchgate to Marine Lines is 2 mins (too short)
    payload = {
        "source": "Churchgate",
        "destination": "Marine Lines",
        "subject": "Data Structures",
        "module": "any module",
        "is_peak": False
    }
    response = client.post("/api/generate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["is_too_short"] is True
    assert "too short" in data["message"]
