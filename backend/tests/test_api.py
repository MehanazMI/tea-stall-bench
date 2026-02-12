"""
Tests for FastAPI endpoints.
"""

import pytest
from unittest.mock import MagicMock, patch, AsyncMock
from fastapi.testclient import TestClient

from backend.main import app
from backend.utils.llm_client import LLMClient
from backend.agents.writer_agent import WriterAgent
from backend.agents.publisher_agent import PublisherAgent


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


@pytest.fixture
def mock_writer_result():
    """Mock writer agent result."""
    return {
        "status": "success",
        "content": "This is a great article about Python tips.",
        "topic": "Python tips",
        "style": "storytelling",
        "word_count": 8
    }


@pytest.fixture
def mock_publisher_result():
    """Mock publisher agent result."""
    return {
        "status": "success",
        "phone_number": "+12345678900",
        "message_length": 42,
        "sent_at": "2026-02-12T01:00:00",
        "delivery_method": "automatic"
    }


class TestHealthEndpoint:
    """Test health check endpoint."""
    
    def test_health_check(self, client):
        """Test health endpoint returns 200 OK."""
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "service" in data
        assert "version" in data


class TestRootEndpoint:
    """Test root endpoint."""
    
    def test_root(self, client):
        """Test root endpoint returns API info."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "name" in data
        assert "docs" in data
        assert "health" in data


class TestStylesEndpoint:
    """Test styles metadata endpoint."""
    
    def test_get_styles(self, client):
        """Test styles endpoint returns available styles."""
        response = client.get("/api/v1/styles")
        assert response.status_code == 200
        data = response.json()
        assert "styles" in data
        assert len(data["styles"]) > 0
        
        # Check structure
        style = data["styles"][0]
        assert "name" in style
        assert "description" in style


class TestChannelsEndpoint:
    """Test channels metadata endpoint."""
    
    def test_get_channels(self, client):
        """Test channels endpoint returns supported channels."""
        response = client.get("/api/v1/channels")
        assert response.status_code == 200
        data = response.json()
        assert "channels" in data
        assert len(data["channels"]) > 0
        
        # Check WhatsApp channel exists
        whatsapp = data["channels"][0]
        assert whatsapp["name"] == "whatsapp"
        assert "max_length" in whatsapp


class TestGenerateEndpoint:
    """Test content generation endpoint."""
    
    @patch('backend.api.v1.routes.WriterAgent')
    def test_generate_success(self, mock_writer_class, client, mock_writer_result):
        """Test successful content generation."""
        # Mock the writer agent
        mock_writer = AsyncMock()
        mock_writer.execute.return_value = mock_writer_result
        mock_writer_class.return_value = mock_writer
        
        response = client.post("/api/v1/generate", json={
            "topic": "Python tips",
            "style": "storytelling"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "content" in data
        assert data["topic"] == "Python tips"
    
    def test_generate_missing_topic(self, client):
        """Test generation fails without topic."""
        response = client.post("/api/v1/generate", json={
            "style": "storytelling"
        })
        assert response.status_code == 422  # Validation error
    
    def test_generate_empty_topic(self, client):
        """Test generation fails with empty topic."""
        response = client.post("/api/v1/generate", json={
            "topic": "ab"  # Too short (min 3 chars)
        })
        assert response.status_code == 422


class TestPublishEndpoint:
    """Test publishing endpoint."""
    
    @patch('backend.api.v1.routes.PublisherAgent')
    def test_publish_success(self, mock_publisher_class, client, mock_publisher_result):
        """Test successful publishing."""
        # Mock the publisher agent
        mock_publisher = AsyncMock()
        mock_publisher.execute.return_value = mock_publisher_result
        mock_publisher_class.return_value = mock_publisher
        
        response = client.post("/api/v1/publish", json={
            "phone_number": "+12345678900",
            "content": "Great Python tip!",
            "auto_send": True
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["phone_number"] == "+12345678900"
        assert data["delivery_method"] == "automatic"
    
    def test_publish_missing_phone(self, client):
        """Test publishing fails without phone number."""
        response = client.post("/api/v1/publish", json={
            "content": "Great Python tip!"
        })
        assert response.status_code == 422
    
    def test_publish_missing_content(self, client):
        """Test publishing fails without content."""
        response = client.post("/api/v1/publish", json={
            "phone_number": "+12345678900"
        })
        assert response.status_code == 422


class TestGenerateAndPublishEndpoint:
    """Test full pipeline endpoint."""
    
    @patch('backend.api.v1.routes.PublisherAgent')
    @patch('backend.api.v1.routes.WriterAgent')
    def test_pipeline_success(self, mock_writer_class, mock_publisher_class, 
                             client, mock_writer_result, mock_publisher_result):
        """Test successful full pipeline."""
        # Mock both agents
        mock_writer = AsyncMock()
        mock_writer.execute.return_value = mock_writer_result
        mock_writer_class.return_value = mock_writer
        
        mock_publisher = AsyncMock()
        mock_publisher.execute.return_value = mock_publisher_result
        mock_publisher_class.return_value = mock_publisher
        
        response = client.post("/api/v1/generate-and-publish", json={
            "topic": "Python tips",
            "phone_number": "+12345678900",
            "style": "storytelling",
            "auto_send": True
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "content" in data
        assert "phone_number" in data
        assert data["delivery_method"] == "automatic"
    
    def test_pipeline_missing_topic(self, client):
        """Test pipeline fails without topic."""
        response = client.post("/api/v1/generate-and-publish", json={
            "phone_number": "+12345678900"
        })
        assert response.status_code == 422
    
    def test_pipeline_missing_phone(self, client):
        """Test pipeline fails without phone number."""
        response = client.post("/api/v1/generate-and-publish", json={
            "topic": "Python tips"
        })
        assert response.status_code == 422

