#!/usr/bin/env python3
"""
Standalone Task 3 Demo - Multi-Agent Calculator App Development

This script demonstrates the exact Task 3 requirements:
1. Sending user message using add_chat_message with AuthorRole.USER
2. Iterating through responses with the specific format:
   async for content in chat.invoke():
       print(f"# {content.role} - {content.name or '*'}: '{content.content}'")
3. Building a calculator app and observing agent collaboration
"""

import asyncio
import os
import sys
from pathlib import Path

# Ensure we can import the multi_agent module
sys.path.insert(0, str(Path(__file__).parent))

# Import required modules (make sure these are installed)
try:
    from multi_agent import run_multi_agent_task3
    print("✅ Successfully imported multi_agent module")
except ImportError as e:
    print(f"❌ Failed to import multi_agent: {e}")
    print("Make sure you're running this from the src/ui directory")
    sys.exit(1)

async def main():
    """
    Main function demonstrating Task 3 requirements exactly as specified.
    """
    
    print("🚀 Task 3: Multi-Agent Calculator App Workflow Demonstration")
    print("=" * 80)
    print("📋 Requirement: Build a calculator app using multi-agent collaboration")
    print("🔧 Implementation:")
    print("   - AuthorRole.USER message sent via add_chat_message")
    print("   - Async iteration through AgentGroupChat.invoke()")
    print("   - Formatted output: # {role} - {name}: '{content}'")
    print("   - Agent collaboration: BusinessAnalyst → SoftwareEngineer → ProductOwner")
    print("=" * 80)
    
    # Task 3 calculator app request
    calculator_request = """I need you to build a calculator app. The calculator should:
1. Have a clean, user-friendly interface
2. Support basic arithmetic operations (addition, subtraction, multiplication, division)
3. Include a clear button to reset calculations
4. Display the current calculation and result clearly
5. Handle decimal numbers
6. Use HTML, CSS, and JavaScript
7. Be responsive and work on different screen sizes

Please create a complete working calculator web application."""
    
    try:
        print(f"🎯 User Request: '{calculator_request[:100]}...'")
        print("=" * 80)
        print("🤖 Starting Multi-Agent Workflow...")
        print("=" * 80)
        
        # Run the Task 3 implementation
        await run_multi_agent_task3(calculator_request)
        
        print("\n" + "=" * 80)
        print("✅ Task 3 Multi-Agent Workflow Completed Successfully!")
        print("📁 Generated Files:")
        print("   - index.html (Calculator web app)")
        print("   - src/ui/push_to_github.sh (Git automation script)")
        print("🚀 The calculator app has been automatically committed and pushed to GitHub!")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n❌ Error during Task 3 execution: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    # Run the async main function
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
