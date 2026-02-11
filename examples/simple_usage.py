"""
Simple example showing how to use the LLM Client

This is a beginner-friendly example that shows you exactly how to use
the LLM Client to get AI responses.
"""

import asyncio
from backend.utils.llm_client import LLMClient


async def simple_example():
    """The simplest possible example."""
    
    # Step 1: Create the client (it reads your .env file automatically!)
    print("📝 Creating LLM Client...")
    client = LLMClient()
    
    # Step 2: Ask the AI to generate something
    print("🤖 Asking AI to write a joke...")
    response = await client.generate("Tell me a short joke about programming")
    
    # Step 3: Print the response
    print("\n✅ AI Response:")
    print(response)


async def advanced_example():
    """A more advanced example with options."""
    
    # Create client
    client = LLMClient()
    
    # Use system prompt to set AI's personality
    print("\n📝 Writing a blog post with a professional tone...")
    response = await client.generate(
        prompt="Write a 2-paragraph blog post about Python programming",
        system_prompt="You are a professional tech blogger",
        temperature=0.7  # Balanced creativity
    )
    
    print("\n✅ AI Response:")
    print(response)


async def error_handling_example():
    """Example showing how to handle errors."""
    
    client = LLMClient()
    
    try:
        # This will work
        response = await client.generate("Hello!")
        print(f"✅ Success: {response}")
        
    except ValueError as e:
        print(f"❌ Validation Error: {e}")
        
    except ConnectionError as e:
        print(f"❌ Connection Error: {e}")
        print("Make sure Ollama is running or your API key is correct!")
        
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")


# Run the examples
if __name__ == "__main__":
    print("=" * 60)
    print("LLM Client - Beginner Examples")
    print("=" * 60)
    
    # Run simple example
    print("\n🔹 EXAMPLE 1: Simple Usage")
    print("-" * 60)
    asyncio.run(simple_example())
    
    # Run advanced example
    print("\n🔹 EXAMPLE 2: Advanced Usage")
    print("-" * 60)
    asyncio.run(advanced_example())
    
    # Run error handling example
    print("\n🔹 EXAMPLE 3: Error Handling")
    print("-" * 60)
    asyncio.run(error_handling_example())
    
    print("\n" + "=" * 60)
    print("✅ Examples complete!")
    print("=" * 60)
