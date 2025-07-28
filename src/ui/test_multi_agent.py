#!/usr/bin/env python3
"""
Test script for Multi-Agent System
Tests the implementation without requiring the full Streamlit UI
"""

import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv

# Add the current directory to path so we can import multi_agent
import sys
sys.path.append(str(Path(__file__).parent))

from multi_agent import run_multi_agent, ApprovalTerminationStrategy

# Load environment variables
load_dotenv()

async def test_multi_agent():
    """Test the multi-agent system with a simple request."""
    
    print("🚀 Testing Multi-Agent System...")
    print("=" * 50)
    
    # Test 1: Basic functionality
    print("Test 1: Basic multi-agent conversation")
    try:
        test_request = "Create a simple HTML page with a welcome message and a button"
        print(f"Request: {test_request}")
        print("-" * 50)
        
        responses = await run_multi_agent(test_request)
        
        print(f"✅ Received {len(responses)} responses from agents:")
        for i, response in enumerate(responses, 1):
            agent_name = response.get('agent', 'Unknown')
            content = response.get('content', 'No content')
            print(f"\n{i}. Agent: {agent_name}")
            print(f"   Response: {content[:200]}..." if len(content) > 200 else f"   Response: {content}")
        
        print("\n" + "=" * 50)
        print("✅ Multi-Agent System test completed successfully!")
        
    except Exception as e:
        print(f"❌ Error testing multi-agent system: {e}")
        import traceback
        traceback.print_exc()

    # Test 2: Termination strategy
    print("\nTest 2: Termination strategy")
    try:
        strategy = ApprovalTerminationStrategy()
        
        # Mock history with approval message
        class MockMessage:
            def __init__(self, content):
                self.content = content
        
        mock_history = [
            MockMessage("This is a test"),
            MockMessage("APPROVED - looks good!"),
            MockMessage("Another message")
        ]
        
        should_terminate = await strategy.should_agent_terminate(None, mock_history)
        print(f"✅ Termination strategy test: {'PASSED' if should_terminate else 'FAILED'}")
        
    except Exception as e:
        print(f"❌ Error testing termination strategy: {e}")

if __name__ == "__main__":
    asyncio.run(test_multi_agent())
