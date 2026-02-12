"""
Tests for FastAPI endpoints.
"""

import pytest
from unittest.mock import patch, AsyncMock
from fastapi.testclient import TestClient

from backend.main import app


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
        assert data["service"] == "Tea Stall Bench API"
        assert data["version"] == "1.0.0"


class TestRootEndpoint:
    """Test root endpoint."""
    
    def test_root(self, client):
        """Test root endpoint returns API info."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Tea Stall Bench API"
        assert data["docs"] == "/docs"
        assert data["health"] == "/api/v1/health"


class TestStylesEndpoint:
    """Test styles metadata endpoint."""
    
    def test_get_styles(self, client):
        """Test styles endpoint returns available styles."""
        response = client.get("/api/v1/styles")
        assert response.status_code == 200
        data = response.json()
        assert "styles" in data
        assert len(data["styles"]) == 6  # Must match WriterAgent.STYLES
        
        # Verify structure and key styles exist
        style_names = [s["name"] for s in data["styles"]]
        assert "storytelling" in style_names
        assert "professional" in style_names
        assert "educational" in style_names
        for style in data["styles"]:
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
        assert len(data["channels"]) >= 1
        
        # Check WhatsApp channel
        whatsapp = data["channels"][0]
        assert whatsapp["name"] == "whatsapp"
        assert whatsapp["requires_phone"] is True
        assert whatsapp["max_length"] == 4000


class TestGenerateEndpoint:
    """Test content generation endpoint."""
    
    @patch('backend.api.v1.routes.WriterAgent')
    def test_generate_success(self, mock_writer_class, client, mock_writer_result):
        """Test successful content generation."""
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
        assert data["content"] == mock_writer_result["content"]
        assert data["topic"] == "Python tips"
        assert data["style"] == "storytelling"
        assert data["word_count"] == 8
    
    def test_generate_missing_topic(self, client):
        """Test generation fails without topic."""
        response = client.post("/api/v1/generate", json={
            "style": "storytelling"
        })
        assert response.status_code == 422
    
    def test_generate_topic_too_short(self, client):
        """Test generation fails with topic under 3 chars."""
        response = client.post("/api/v1/generate", json={
            "topic": "ab"
        })
        assert response.status_code == 422
    
    @patch('backend.api.v1.routes.WriterAgent')
    def test_generate_default_style(self, mock_writer_class, client, mock_writer_result):
        """Test generation uses default storytelling style."""
        mock_writer = AsyncMock()
        mock_writer.execute.return_value = mock_writer_result
        mock_writer_class.return_value = mock_writer
        
        response = client.post("/api/v1/generate", json={
            "topic": "Python tips"
        })
        
        assert response.status_code == 200
        # Verify writer was called with storytelling default
        call_args = mock_writer.execute.call_args[0][0]
        assert call_args["style"] == "storytelling"


class TestPublishEndpoint:
    """Test publishing endpoint."""
    
    @patch('backend.api.v1.routes.PublisherAgent')
    def test_publish_success(self, mock_publisher_class, client, mock_publisher_result):
        """Test successful publishing."""
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
        assert data["message_length"] == 42
    
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
    
    @patch('backend.api.v1.routes.PublisherAgent')
    def test_publish_manual_review(self, mock_publisher_class, client):
        """Test publishing with manual review mode."""
        mock_publisher = AsyncMock()
        mock_publisher.execute.return_value = {
            "status": "success",
            "phone_number": "+12345678900",
            "message_length": 20,
            "sent_at": None,
            "delivery_method": "manual_review"
        }
        mock_publisher_class.return_value = mock_publisher
        
        response = client.post("/api/v1/publish", json={
            "phone_number": "+12345678900",
            "content": "Test content",
            "auto_send": False
        })
        
        assert response.status_code == 200
        assert response.json()["delivery_method"] == "manual_review"


class TestGenerateAndPublishEndpoint:
    """Test full pipeline endpoint."""
    
    @patch('backend.api.v1.routes.PublisherAgent')
    @patch('backend.api.v1.routes.WriterAgent')
    def test_pipeline_success(self, mock_writer_class, mock_publisher_class, 
                             client, mock_writer_result, mock_publisher_result):
        """Test successful full pipeline."""
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
        assert data["content"] == mock_writer_result["content"]
        assert data["phone_number"] == "+12345678900"
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

    @patch('backend.api.v1.routes.WriterAgent')
    def test_pipeline_writer_error_returns_500(self, mock_writer_class, client):
        """Test pipeline returns 500 when writer fails."""
        mock_writer = AsyncMock()
        mock_writer.execute.side_effect = Exception("LLM unavailable")
        mock_writer_class.return_value = mock_writer
        
        response = client.post("/api/v1/generate-and-publish", json={
            "topic": "Python tips",
            "phone_number": "+12345678900"
        })
        
        assert response.status_code == 500
        assert "Pipeline failed" in response.json()["detail"]
