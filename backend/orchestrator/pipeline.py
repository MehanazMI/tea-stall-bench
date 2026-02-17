"""
Pipeline Orchestrator (Director) for Tea Stall Bench

Manages the Research → Outline → Write pipeline.
Persona: 'Director' / 'Iyakkunar' (Tamil: Director)
"""

import logging
import uuid
from typing import Dict, Any, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field

from backend.agents.research_agent import ResearchAgent
from backend.agents.outline_agent import OutlineAgent
from backend.agents.writer_agent import WriterAgent
from backend.utils.llm_client import LLMClient

logger = logging.getLogger(__name__)


class PipelineContext(BaseModel):
    """
    Immutable state container for the pipeline execution.
    Tracks data flow between agents and any errors encountered.
    """
    trace_id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    topic: str
    content_type: str = "blog"
    style: str = "professional"
    length: str = "medium"
    channel: str = "blog"

    # Agent outputs (populated sequentially)
    research_data: Optional[str] = None
    research_sources: Optional[List[str]] = None
    outline: Optional[Dict[str, Any]] = None
    article_title: Optional[str] = None
    article_content: Optional[str] = None
    word_count: Optional[int] = None

    # Status tracking
    current_stage: str = "initialized"
    errors: List[str] = Field(default_factory=list)
    started_at: Optional[str] = None
    completed_at: Optional[str] = None


class Orchestrator:
    """
    Pipeline Orchestrator (Director).
    
    Coordinates the execution of: Scout (Research) → Draft (Outline) → Ink (Write).
    Handles errors gracefully, allowing the pipeline to continue even if
    research fails (falls back to general knowledge).
    """

    def __init__(self, llm_client: LLMClient):
        if not llm_client:
            raise ValueError("LLM client is required for Orchestrator")

        self.llm_client = llm_client
        self.logger = logging.getLogger("TeaStallBench.Director")

        # Initialize agents
        self.scout = ResearchAgent(client=llm_client)
        self.draft = OutlineAgent(llm_client=llm_client)
        self.ink = WriterAgent(llm_client=llm_client)

        self.logger.info("Director initialized with Scout, Draft, and Ink agents")

    async def run_pipeline(
        self,
        topic: str,
        content_type: str = "blog",
        style: str = "professional",
        length: str = "medium",
        channel: str = "blog"
    ) -> PipelineContext:
        """
        Execute the full content pipeline: Research → Outline → Write.

        Args:
            topic: The topic to create content about
            content_type: Type of content (blog, post, tutorial, etc.)
            style: Writing style (professional, friendly, etc.)
            length: Desired length (short, medium, long)
            channel: Publishing channel (blog, whatsapp, etc.)

        Returns:
            PipelineContext with all collected data and final article
        """
        ctx = PipelineContext(
            topic=topic,
            content_type=content_type,
            style=style,
            length=length,
            channel=channel,
            started_at=datetime.now().isoformat()
        )

        self.logger.info(f"[{ctx.trace_id}] 🎬 Pipeline started for topic: '{topic}'")

        # ── Stage 1: Research (Scout) ──────────────────────────────
        ctx = await self._stage_research(ctx)

        # ── Stage 2: Outline (Draft) ──────────────────────────────
        ctx = await self._stage_outline(ctx)

        # ── Stage 3: Write (Ink) ──────────────────────────────────
        ctx = await self._stage_write(ctx)

        # ── Done ──────────────────────────────────────────────────
        ctx.current_stage = "completed"
        ctx.completed_at = datetime.now().isoformat()

        self.logger.info(f"[{ctx.trace_id}] ✅ Pipeline completed. Word count: {ctx.word_count}")
        if ctx.errors:
            self.logger.warning(f"[{ctx.trace_id}] ⚠️ Pipeline had {len(ctx.errors)} non-fatal error(s)")

        return ctx

    async def _stage_research(self, ctx: PipelineContext) -> PipelineContext:
        """Stage 1: Research via Scout agent."""
        ctx.current_stage = "researching"
        self.logger.info(f"[{ctx.trace_id}] 🔍 Stage 1: Scout researching '{ctx.topic}'...")

        try:
            result = await self.scout.execute({"topic": ctx.topic})
            ctx.research_data = result.get("research_data", "")
            ctx.research_sources = result.get("sources", [])
            self.logger.info(f"[{ctx.trace_id}] 🔍 Research complete. Sources: {len(ctx.research_sources or [])}")
        except Exception as e:
            error_msg = f"Research failed: {str(e)}"
            ctx.errors.append(error_msg)
            ctx.research_data = f"General knowledge about: {ctx.topic}"
            self.logger.warning(f"[{ctx.trace_id}] ⚠️ {error_msg}. Falling back to general knowledge.")

        return ctx

    async def _stage_outline(self, ctx: PipelineContext) -> PipelineContext:
        """Stage 2: Generate outline via Draft agent."""
        ctx.current_stage = "outlining"
        self.logger.info(f"[{ctx.trace_id}] 📝 Stage 2: Draft creating outline...")

        try:
            result = await self.draft.execute({
                "topic": ctx.topic,
                "research_data": ctx.research_data or ""
            })
            ctx.outline = result.get("outline", {})
            self.logger.info(f"[{ctx.trace_id}] 📝 Outline complete. Sections: {len(ctx.outline.get('sections', []))}")
        except Exception as e:
            error_msg = f"Outline failed: {str(e)}"
            ctx.errors.append(error_msg)
            ctx.outline = {
                "title": ctx.topic,
                "sections": [
                    {"heading": "Introduction", "key_points": [f"Overview of {ctx.topic}"]},
                    {"heading": "Key Points", "key_points": [f"Main ideas about {ctx.topic}"]},
                    {"heading": "Conclusion", "key_points": ["Summary and takeaways"]}
                ]
            }
            self.logger.warning(f"[{ctx.trace_id}] ⚠️ {error_msg}. Using fallback outline.")

        return ctx

    async def _stage_write(self, ctx: PipelineContext) -> PipelineContext:
        """Stage 3: Generate article via Ink (Writer) agent."""
        ctx.current_stage = "writing"
        self.logger.info(f"[{ctx.trace_id}] ✍️ Stage 3: Ink writing article...")

        import json as json_mod
        additional_context = ""
        if ctx.research_data:
            additional_context += f"Research Summary:\n{ctx.research_data[:2000]}\n\n"
        if ctx.outline:
            additional_context += f"Content Outline:\n{json_mod.dumps(ctx.outline, indent=2)}\n"

        try:
            result = await self.ink.execute({
                "topic": ctx.topic,
                "content_type": ctx.content_type,
                "style": ctx.style,
                "length": ctx.length,
                "channel": ctx.channel,
                "additional_context": additional_context
            })
            ctx.article_title = result.get("title", ctx.topic)
            ctx.article_content = result.get("content", "")
            ctx.word_count = result.get("word_count", 0)
            self.logger.info(f"[{ctx.trace_id}] ✍️ Article complete. Title: '{ctx.article_title}'")
        except Exception as e:
            error_msg = f"Writing failed: {str(e)}"
            ctx.errors.append(error_msg)
            self.logger.error(f"[{ctx.trace_id}] ❌ {error_msg}")

        return ctx
