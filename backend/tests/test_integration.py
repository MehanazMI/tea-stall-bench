"""
End-to-end integration tests for Tea Stall Bench.

Tests the full pipeline: API → Writer Agent → Publisher Agent
"""

import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from fastapi.testclient import TestClient

from backend.main import app
from backend.utils.llm_client import LLMClient
from backend.agents.writer_agent import WriterAgent
from backend.agents.publisher_agent import PublisherAgent


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


class TestFullPipeline:
    """Test the complete generate-and-publish pipeline."""
    
    @patch('backend.api.v1.routes.PublisherAgent')
    @patch('backend.api.v1.routes.WriterAgent')
    def test_full_pipeline_storytelling(self, mock_writer_class, mock_publisher_class, client):
        """Test full pipeline with storytelling style."""
        # Mock Writer
        mock_writer = AsyncMock()
        mock_writer.execute.return_value = {
            "status": "success",
            "content": "Once upon a time, Python was born...",
            "topic": "Python history",
            "style": "storytelling",
            "word_count": 7
        }
        mock_writer_class.return_value = mock_writer
        
        # Mock Publisher
        mock_publisher = AsyncMock()
        mock_publisher.execute.return_value = {
            "status": "success",
            "phone_number": "+12345678900",
            "message_length": 35,
            "sent_at": "2026-02-12T17:00:00",
            "delivery_method": "automatic"
        }
        mock_publisher_class.return_value = mock_publisher
        
        # Execute pipeline
        response = client.post("/api/v1/generate-and-publish", json={
            "topic": "Python history",
            "phone_number": "+12345678900",
            "style": "storytelling",
            "auto_send": True
        })
        
        # Verify success
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["topic"] == "Python history"
        assert "content" in data
        assert data["phone_number"] == "+12345678900"
        assert data["delivery_method"] == "automatic"
        
        # Verify Writer was called with correct args
        writer_call = mock_writer.execute.call_args[0][0]
        assert writer_call["topic"] == "Python history"
        assert writer_call["style"] == "storytelling"
        
        # Verify Publisher received Writer's content
        publisher_call = mock_publisher.execute.call_args[0][0]
        assert publisher_call["content"] == "Once upon a time, Python was born..."
        assert publisher_call["phone_number"] == "+12345678900"
        assert publisher_call["auto_send"] is True
    
    @patch('backend.api.v1.routes.PublisherAgent')
    @patch('backend.api.v1.routes.WriterAgent')
    def test_full_pipeline_manual_review(self, mock_writer_class, mock_publisher_class, client):
        """Test pipeline with manual review mode."""
        mock_writer = AsyncMock()
        mock_writer.execute.return_value = {
            "status": "success",
            "content": "Top 5 meditation tips...",
            "topic": "Meditation tips",
            "style": "educational",
            "word_count": 5
        }
        mock_writer_class.return_value = mock_writer
        
        mock_publisher = AsyncMock()
        mock_publisher.execute.return_value = {
            "status": "success",
            "phone_number": "+919876543210",
            "message_length": 25,
            "sent_at": None,
            "delivery_method": "manual_review"
        }
        mock_publisher_class.return_value = mock_publisher
        
        response = client.post("/api/v1/generate-and-publish", json={
            "topic": "Meditation tips",
            "phone_number": "+919876543210",
            "style": "educational",
            "auto_send": False
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["delivery_method"] == "manual_review"
        assert data["phone_number"] == "+919876543210"
    
    @patch('backend.api.v1.routes.WriterAgent')
    def test_pipeline_fails_on_writer_error(self, mock_writer_class, client):
        """Test pipeline handles Writer failure gracefully."""
        mock_writer = AsyncMock()
        mock_writer.execute.side_effect = Exception("LLM unavailable")
        mock_writer_class.return_value = mock_writer
        
        response = client.post("/api/v1/generate-and-publish", json={
            "topic": "Python tips",
            "phone_number": "+12345678900"
        })
        
        assert response.status_code == 500
        assert "Pipeline failed" in response.json()["detail"]
    
    @patch('backend.api.v1.routes.PublisherAgent')
    @patch('backend.api.v1.routes.WriterAgent')
    def test_pipeline_fails_on_publisher_error(self, mock_writer_class, mock_publisher_class, client):
        """Test pipeline handles Publisher failure gracefully."""
        mock_writer = AsyncMock()
        mock_writer.execute.return_value = {
            "status": "success",
            "content": "Great article",
            "topic": "Test",
            "style": "casual",
            "word_count": 2
        }
        mock_writer_class.return_value = mock_writer
        
        mock_publisher = AsyncMock()
        mock_publisher.execute.side_effect = Exception("WhatsApp unavailable")
        mock_publisher_class.return_value = mock_publisher
        
        response = client.post("/api/v1/generate-and-publish", json={
            "topic": "Test topic",
            "phone_number": "+12345678900"
        })
        
        assert response.status_code == 500
        assert "Pipeline failed" in response.json()["detail"]


class TestGenerateAndPublishSeparately:
    """Test generate then publish as separate API calls."""
    
    @patch('backend.api.v1.routes.PublisherAgent')
    @patch('backend.api.v1.routes.WriterAgent')
    def test_generate_then_publish(self, mock_writer_class, mock_publisher_class, client):
        """Test calling generate and publish separately."""
        # Step 1: Generate
        mock_writer = AsyncMock()
        mock_writer.execute.return_value = {
            "status": "success",
            "content": "Python is amazing for beginners!",
            "topic": "Python for beginners",
            "style": "casual",
            "word_count": 5
        }
        mock_writer_class.return_value = mock_writer
        
        gen_response = client.post("/api/v1/generate", json={
            "topic": "Python for beginners",
            "style": "casual"
        })
        
        assert gen_response.status_code == 200
        generated_content = gen_response.json()["content"]
        
        # Step 2: Publish the generated content
        mock_publisher = AsyncMock()
        mock_publisher.execute.return_value = {
            "status": "success",
            "phone_number": "+12345678900",
            "message_length": len(generated_content),
            "sent_at": "2026-02-12T17:00:00",
            "delivery_method": "automatic"
        }
        mock_publisher_class.return_value = mock_publisher
        
        pub_response = client.post("/api/v1/publish", json={
            "phone_number": "+12345678900",
            "content": generated_content,
            "title": "Python Tip",
            "auto_send": True
        })
        
        assert pub_response.status_code == 200
        assert pub_response.json()["delivery_method"] == "automatic"


class TestAllEndpointsExist:
    """Verify all endpoints respond correctly."""
    
    def test_health_responds(self, client):
        """Health endpoint should always work."""
        assert client.get("/api/v1/health").status_code == 200
    
    def test_styles_responds(self, client):
        """Styles endpoint should always work."""
        response = client.get("/api/v1/styles")
        assert response.status_code == 200
        styles = [s["name"] for s in response.json()["styles"]]
        assert "storytelling" in styles
        assert "professional" in styles
    
    def test_channels_responds(self, client):
        """Channels endpoint should always work."""
        response = client.get("/api/v1/channels")
        assert response.status_code == 200
        assert response.json()["channels"][0]["name"] == "whatsapp"
    
    def test_root_responds(self, client):
        """Root endpoint should show API info."""
        response = client.get("/")
        assert response.status_code == 200
        assert response.json()["name"] == "Tea Stall Bench API"
    
    def test_docs_available(self, client):
        """Swagger docs should be available."""
        response = client.get("/docs")
        assert response.status_code == 200
