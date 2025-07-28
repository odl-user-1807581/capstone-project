#!/usr/bin/env python3
"""
Task 3 Runner: Multi-Agent Calculator App Development

This script runs the Task 3 implementation to demonstrate the multi-agent workflow
for building a calculator app with proper message formatting as required.
"""

import asyncio
import sys
from pathlib import Path

# Add the current directory to the path so we can import multi_agent
sys.path.insert(0, str(Path(__file__).parent))

from multi_agent import run_multi_agent_task3

async def run_calculator_demo():
    """Run the calculator app development demo."""
    
    calculator_request = """
I need you to build a calculator app. The calculator should:
1. Have a clean, user-friendly interface
2. Support basic arithmetic operations (addition, subtraction, multiplication, division)
3. Include a clear button to reset calculations
4. Display the current calculation and result clearly
5. Handle decimal numbers
6. Use HTML, CSS, and JavaScript
7. Be responsive and work on different screen sizes

Please create a complete working calculator web application.
"""
    
    print("🚀 Task 3: Multi-Agent Calculator App Development")
    print("=" * 80)
    print("📋 Request: Building a calculator web application")
    print("🤖 Agents: BusinessAnalyst → SoftwareEngineer → ProductOwner")
    print("=" * 80)
    
    try:
        await run_multi_agent_task3(calculator_request)
        print("\n✅ Task 3 completed successfully!")
        print("📁 Check for generated files: index.html and src/ui/push_to_github.sh")
        
    except Exception as e:
        print(f"\n❌ Error during Task 3 execution: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(run_calculator_demo())
