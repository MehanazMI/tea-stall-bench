"""
Tests for Enhanced Writer Agent (Ink 2.0)

Tests outline-aware prompt building, compliance checking, and
integration with the pipeline orchestrator.
"""

import re
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from backend.agents.writer_agent import WriterAgent
from backend.utils.llm_client import LLMClient


# ── Fixtures ─────────────────────────────────────────────────

@pytest.fixture
def mock_llm():
    """Create a mock LLM client."""
    client = MagicMock(spec=LLMClient)
    client.generate = AsyncMock()
    return client


@pytest.fixture
def writer(mock_llm):
    """Create a WriterAgent with mocked LLM."""
    return WriterAgent(llm_client=mock_llm)


@pytest.fixture
def sample_outline():
    """Standard 3-section outline from Draft agent."""
    return {
        "title": "The Future of AI",
        "sections": [
            {"heading": "Introduction", "key_points": ["Overview of AI trends"]},
            {"heading": "Current Landscape", "key_points": ["Major players", "Key technologies"]},
            {"heading": "Conclusion", "key_points": ["Summary and predictions"]}
        ]
    }


# ── Prompt Building Tests ─────────────────────────────────────

class TestOutlineAwarePrompt:
    """Test that _build_prompt injects outline sections as structured instructions."""

    def test_prompt_without_outline(self, writer):
        """Without outline, prompt should NOT contain structure instructions."""
        prompt = writer._build_prompt(
            topic="AI", content_type="blog", style="friendly",
            length="short", channel="blog", additional_context=""
        )
        assert "MUST follow this exact structure" not in prompt

    def test_prompt_with_outline(self, writer, sample_outline):
        """With outline, prompt should contain structured section instructions."""
        prompt = writer._build_prompt(
            topic="AI", content_type="blog", style="friendly",
            length="short", channel="blog", additional_context="",
            outline=sample_outline
        )
        assert "MUST follow this exact structure" in prompt
        assert "Section 1: Introduction" in prompt
        assert "Section 2: Current Landscape" in prompt
        assert "Section 3: Conclusion" in prompt

    def test_prompt_includes_key_points(self, writer, sample_outline):
        """Key points should be included in section instructions."""
        prompt = writer._build_prompt(
            topic="AI", content_type="blog", style="friendly",
            length="short", channel="blog", additional_context="",
            outline=sample_outline
        )
        assert "Overview of AI trends" in prompt
        assert "Major players" in prompt

    def test_prompt_with_empty_outline(self, writer):
        """Empty outline should behave like no outline."""
        prompt = writer._build_prompt(
            topic="AI", content_type="blog", style="friendly",
            length="short", channel="blog", additional_context="",
            outline={"title": "Test", "sections": []}
        )
        assert "MUST follow this exact structure" not in prompt

    def test_prompt_preserves_additional_context(self, writer, sample_outline):
        """Additional context should still be included alongside outline."""
        prompt = writer._build_prompt(
            topic="AI", content_type="blog", style="friendly",
            length="short", channel="blog",
            additional_context="Research: AI is growing fast",
            outline=sample_outline
        )
        assert "Research: AI is growing fast" in prompt
        assert "Section 1: Introduction" in prompt


# ── Compliance Check Tests ────────────────────────────────────

class TestComplianceCheck:
    """Test _check_compliance scoring logic."""

    def test_full_coverage(self, writer, sample_outline):
        """All headings present = 100% score."""
        content = """
        ## Introduction
        AI is transforming everything.
        
        ## Current Landscape
        Major players include OpenAI, Google, Meta.
        
        ## Conclusion
        The future is bright.
        """
        result = writer._check_compliance(content, sample_outline)
        assert result['score'] == 1.0
        assert len(result['covered']) == 3
        assert len(result['missing']) == 0

    def test_partial_coverage(self, writer, sample_outline):
        """Some headings missing = partial score."""
        content = """
        ## Introduction
        AI is transforming everything.
        
        ## Conclusion
        The future is bright.
        """
        result = writer._check_compliance(content, sample_outline)
        # "Current Landscape" is missing but partial match via "Landscape" (>3 chars)
        # may still pass. Let's check:
        assert result['score'] > 0
        assert len(result['covered']) >= 2

    def test_no_coverage(self, writer):
        """No headings present = 0% score."""
        outline = {
            "sections": [
                {"heading": "Xylophone", "key_points": []},
                {"heading": "Zeppelin", "key_points": []}
            ]
        }
        content = "This article talks about nothing relevant."
        result = writer._check_compliance(content, outline)
        assert result['score'] == 0.0
        assert len(result['missing']) == 2

    def test_empty_outline_full_score(self, writer):
        """Empty outline = 100% by default."""
        result = writer._check_compliance("any content", {"sections": []})
        assert result['score'] == 1.0

    def test_case_insensitive(self, writer):
        """Matching should be case-insensitive."""
        outline = {"sections": [{"heading": "INTRODUCTION", "key_points": []}]}
        content = "This introduction covers the basics."
        result = writer._check_compliance(content, outline)
        assert result['score'] == 1.0
        assert "INTRODUCTION" in result['covered']

    def test_partial_word_match(self, writer):
        """Headings with >3 char words should partial-match."""
        outline = {"sections": [{"heading": "Advanced Technology Trends", "key_points": []}]}
        content = "The technology sector is evolving rapidly."
        result = writer._check_compliance(content, outline)
        assert result['score'] == 1.0  # "Technology" matches


# ── Integration Tests ─────────────────────────────────────────

class TestWriterWithOutline:
    """Test _execute_internal with outline context."""

    @pytest.mark.asyncio
    async def test_execution_with_outline_returns_compliance(self, writer, mock_llm, sample_outline):
        """When outline is provided, result should include compliance dict."""
        mock_llm.generate.return_value = (
            "The Future of AI\n\n"
            "## Introduction\nAI is here.\n\n"
            "## Current Landscape\nMany players.\n\n"
            "## Conclusion\nLooking ahead."
        )
        result = await writer.execute({
            "topic": "AI",
            "outline": sample_outline
        })
        assert 'compliance' in result
        assert result['compliance']['score'] > 0

    @pytest.mark.asyncio
    async def test_execution_without_outline_no_compliance(self, writer, mock_llm):
        """Without outline, result should NOT include compliance."""
        mock_llm.generate.return_value = "Title Here\n\nSome content about the topic."
        result = await writer.execute({
            "topic": "AI"
        })
        assert 'compliance' not in result

    @pytest.mark.asyncio
    async def test_execution_prompt_contains_outline(self, writer, mock_llm, sample_outline):
        """The prompt sent to LLM should contain outline section instructions."""
        mock_llm.generate.return_value = "Title\n\nContent about Introduction and Conclusion"
        await writer.execute({
            "topic": "AI",
            "outline": sample_outline
        })
        # Check what prompt was sent to generate()
        call_args = mock_llm.generate.call_args
        prompt = call_args.kwargs.get('prompt', call_args.args[0] if call_args.args else '')
        assert "Section 1: Introduction" in prompt
        assert "MUST follow this exact structure" in prompt
