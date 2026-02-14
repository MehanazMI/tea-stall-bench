#!/usr/bin/env python3
"""
Tea Stall Bench CLI - Quick Content Generation & Publishing

Usage:
    python -m backend.cli generate "Python tips"
    python -m backend.cli generate "Meditation benefits" --style professional
    python -m backend.cli publish "+12345678900" "Hello World!"
    python -m backend.cli pipeline "Python tips" "+12345678900"
    python -m backend.cli pipeline "Python tips" "+12345678900" --review
"""

import asyncio
import argparse
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.utils.llm_client import LLMClient
from backend.agents.writer_agent import WriterAgent
from backend.agents.publisher_agent import PublisherAgent

# Available styles (synced with WriterAgent.STYLES)
STYLES = ["technical", "educational", "professional", "friendly", "inspirational", "storytelling"]


def create_parser():
    """Create argument parser."""
    parser = argparse.ArgumentParser(
        prog="tea-stall-bench",
        description="🍵 Tea Stall Bench - AI Content Generator & WhatsApp Publisher"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Generate command
    gen_parser = subparsers.add_parser("generate", help="Generate content from a topic")
    gen_parser.add_argument("topic", help="Topic to write about")
    gen_parser.add_argument("--style", default="storytelling", 
                           choices=STYLES,
                           help="Writing style (default: storytelling)")
    
    # Publish command
    pub_parser = subparsers.add_parser("publish", help="Publish content to WhatsApp")
    pub_parser.add_argument("phone", help="Phone number with country code (e.g. +12345678900)")
    pub_parser.add_argument("content", help="Content to publish")
    pub_parser.add_argument("--title", default=None, help="Optional title")
    pub_parser.add_argument("--review", action="store_true", 
                           help="Manual review mode (don't auto-send)")
    
    # Pipeline command (generate + publish)
    pipe_parser = subparsers.add_parser("pipeline", help="Generate and publish in one step")
    pipe_parser.add_argument("topic", help="Topic to write about")
    pipe_parser.add_argument("phone", help="Phone number with country code (e.g. +12345678900)")
    pipe_parser.add_argument("--style", default="storytelling",
                            choices=STYLES,
                            help="Writing style (default: storytelling)")
    pipe_parser.add_argument("--title", default=None, help="Optional title")
    pipe_parser.add_argument("--review", action="store_true",
                            help="Manual review mode (don't auto-send)")
    
    return parser


async def cmd_generate(args):
    """Generate content from topic."""
    print(f"\n🍵 Generating content about: {args.topic}")
    print(f"   Style: {args.style}\n")
    
    llm_client = LLMClient()
    writer = WriterAgent(llm_client)
    
    result = await writer.execute({
        "topic": args.topic,
        "style": args.style
    })
    
    print("=" * 60)
    print(f"📝 Generated Content ({result['word_count']} words)")
    print("=" * 60)
    print(result["content"])
    print("=" * 60)
    
    return result


async def cmd_publish(args):
    """Publish content to WhatsApp."""
    print(f"\n📱 Publishing to: {args.phone}")
    mode = "Manual Review" if args.review else "Automatic"
    print(f"   Mode: {mode}\n")
    
    llm_client = LLMClient()
    publisher = PublisherAgent(llm_client)
    
    result = await publisher.execute({
        "phone_number": args.phone,
        "content": args.content,
        "title": args.title,
        "auto_send": not args.review
    })
    
    print(f"✅ Published! Method: {result['delivery_method']}")
    return result


async def cmd_pipeline(args):
    """Generate and publish in one step."""
    print(f"\n🍵 Pipeline: {args.topic} → {args.phone}")
    print(f"   Style: {args.style}")
    mode = "Manual Review" if args.review else "Automatic"
    print(f"   Mode: {mode}\n")
    
    llm_client = LLMClient()
    writer = WriterAgent(llm_client)
    publisher = PublisherAgent(llm_client)
    
    # Step 1: Generate
    print("Step 1: Generating content...")
    gen_result = await writer.execute({
        "topic": args.topic,
        "style": args.style
    })
    
    print(f"   ✅ Generated {gen_result['word_count']} words\n")
    print("=" * 60)
    print(gen_result["content"])
    print("=" * 60)
    
    # Step 2: Publish
    print("\nStep 2: Publishing to WhatsApp...")
    pub_result = await publisher.execute({
        "phone_number": args.phone,
        "content": gen_result["content"],
        "title": args.title,
        "auto_send": not args.review
    })
    
    print(f"   ✅ Published! Method: {pub_result['delivery_method']}")
    print(f"\n🎉 Done! Content delivered to {args.phone}")
    
    return gen_result, pub_result


def main():
    """Main entry point."""
    parser = create_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        print("\n🍵 Example commands:")
        print('  python -m backend.cli generate "Python tips"')
        print('  python -m backend.cli publish "+12345678900" "Hello!"')
        print('  python -m backend.cli pipeline "Python tips" "+12345678900"')
        sys.exit(1)
    
    try:
        if args.command == "generate":
            asyncio.run(cmd_generate(args))
        elif args.command == "publish":
            asyncio.run(cmd_publish(args))
        elif args.command == "pipeline":
            asyncio.run(cmd_pipeline(args))
    except KeyboardInterrupt:
        print("\n\nCancelled.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
