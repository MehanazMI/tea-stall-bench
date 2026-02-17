"""
Test script for Hybrid Search Provider (Circuit Breaker Logic)
"""
import sys
import os
import logging
from unittest.mock import MagicMock

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.utils.search_client import HybridSearchProvider, SearchProvider

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MockProvider(SearchProvider):
    def __init__(self, name, should_fail=False):
        self.name = name
        self.should_fail = should_fail
        
    def search(self, query: str) -> str:
        if self.should_fail:
            raise Exception(f"{self.name} failed explicitly!")
        return f"Results from {self.name} for '{query}'"

def test_primary_success():
    print("\n--- Testing Primary Success ---")
    primary = MockProvider("Primary", should_fail=False)
    fallback = MockProvider("Fallback", should_fail=False)
    hybrid = HybridSearchProvider(primary, fallback)
    
    result = hybrid.search("test query")
    print(f"Result: {result}")
    assert "Primary" in result
    print("✅ Primary success test passed")

def test_fallback_success():
    print("\n--- Testing Fallback Logic ---")
    primary = MockProvider("Primary", should_fail=True)
    fallback = MockProvider("Fallback", should_fail=False)
    hybrid = HybridSearchProvider(primary, fallback)
    
    result = hybrid.search("test query")
    print(f"Result: {result}")
    assert "Fallback" in result
    print("✅ Fallback success test passed")

def test_both_fail():
    print("\n--- Testing Both Fail ---")
    primary = MockProvider("Primary", should_fail=True)
    fallback = MockProvider("Fallback", should_fail=True)
    hybrid = HybridSearchProvider(primary, fallback)
    
    try:
        hybrid.search("test query")
        print("❌ Should have raised exception")
    except Exception as e:
        print(f"✅ Caught expected exception: {e}")

if __name__ == "__main__":
    test_primary_success()
    test_fallback_success()
    test_both_fail()
