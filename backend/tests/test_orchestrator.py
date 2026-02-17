"""
Unit tests for Pipeline Orchestrator (Director)
"""
import pytest
import json
from unittest.mock import AsyncMock, MagicMock, patch
from backend.orchestrator import Orchestrator, PipelineContext
from backend.utils.llm_client import LLMClient


class TestPipelineContext:
    """Test PipelineContext model."""

    def test_context_creation(self):
        ctx = PipelineContext(topic="Test Topic")
        assert ctx.topic == "Test Topic"
        assert ctx.current_stage == "initialized"
        assert ctx.errors == []
        assert ctx.trace_id  # auto-generated

    def test_context_defaults(self):
        ctx = PipelineContext(topic="AI")
        assert ctx.content_type == "blog"
        assert ctx.style == "professional"
        assert ctx.length == "medium"
        assert ctx.channel == "blog"


class TestOrchestratorInit:
    """Test Orchestrator initialization."""

    def test_init_with_client(self):
        mock_client = MagicMock(spec=LLMClient)
        orch = Orchestrator(mock_client)
        assert orch.scout is not None
        assert orch.draft is not None
        assert orch.ink is not None

    def test_init_without_client(self):
        with pytest.raises(ValueError, match="LLM client is required"):
            Orchestrator(None)


class TestOrchestratorPipeline:
    """Test full pipeline execution."""

    @pytest.mark.asyncio
    async def test_successful_pipeline(self):
        """Test pipeline completes successfully with all three stages."""
        mock_client = AsyncMock(spec=LLMClient)

        # Mock LLM responses for each stage:
        # 1. Research (Scout) uses search + LLM summary
        # 2. Outline (Draft) returns JSON
        # 3. Writer (Ink) returns article text
        outline_json = json.dumps({
            "title": "Test Outline",
            "sections": [
                {"heading": "Intro", "key_points": ["Point A"]},
                {"heading": "Body", "key_points": ["Point B"]}
            ]
        })

        mock_client.generate.side_effect = [
            "Research summary about AI agents...",  # Scout's LLM call
            outline_json,                            # Draft's LLM call
            "The Future of AI\n\nAI is transforming..."  # Ink's LLM call
        ]

        with patch('backend.agents.research_agent.get_search_provider') as mock_search:
            mock_provider = MagicMock()
            mock_provider.search.return_value = "Search results about AI"
            mock_search.return_value = mock_provider

            orch = Orchestrator(mock_client)
            ctx = await orch.run_pipeline("AI Agents")

        assert ctx.current_stage == "completed"
        assert ctx.research_data is not None
        assert ctx.outline is not None
        assert ctx.article_content is not None
        assert ctx.word_count is not None
        assert len(ctx.errors) == 0

    @pytest.mark.asyncio
    async def test_pipeline_research_failure_continues(self):
        """Test pipeline continues even when research fails."""
        mock_client = AsyncMock(spec=LLMClient)

        outline_json = json.dumps({
            "title": "Fallback Outline",
            "sections": [{"heading": "Intro", "key_points": ["General point"]}]
        })

        mock_client.generate.side_effect = [
            outline_json,                                # Draft's LLM call
            "Fallback Article\n\nGeneral knowledge..."   # Ink's LLM call
        ]

        with patch('backend.agents.research_agent.get_search_provider') as mock_search:
            mock_provider = MagicMock()
            mock_provider.search.side_effect = Exception("Network error")
            mock_search.return_value = mock_provider

            orch = Orchestrator(mock_client)
            ctx = await orch.run_pipeline("Test Topic")

        assert ctx.current_stage == "completed"
        assert len(ctx.errors) >= 1
        assert "Research failed" in ctx.errors[0]
        assert ctx.article_content is not None  # Pipeline still completed

    @pytest.mark.asyncio
    async def test_pipeline_outline_failure_uses_fallback(self):
        """Test pipeline uses fallback outline when Draft fails."""
        mock_client = AsyncMock(spec=LLMClient)

        # Scout succeeds, Draft fails (bad JSON x3), Ink succeeds
        mock_client.generate.side_effect = [
            "Research data...",         # Scout's LLM
            "NOT VALID JSON",           # Draft attempt 1
            "STILL NOT JSON",           # Draft attempt 2
            "NOPE",                     # Draft attempt 3
            "Article Title\n\nContent"  # Ink's LLM
        ]

        with patch('backend.agents.research_agent.get_search_provider') as mock_search:
            mock_provider = MagicMock()
            mock_provider.search.return_value = "Search results"
            mock_search.return_value = mock_provider

            orch = Orchestrator(mock_client)
            ctx = await orch.run_pipeline("Test Topic")

        assert ctx.current_stage == "completed"
        assert len(ctx.errors) >= 1
        assert "Outline failed" in ctx.errors[0]
        # Fallback outline was used
        assert ctx.outline is not None
        assert ctx.outline["sections"][0]["heading"] == "Introduction"
