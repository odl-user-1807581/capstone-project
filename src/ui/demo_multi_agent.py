#!/usr/bin/env python3
"""
Multi-Agent System Demo
Demonstrates the complete workflow including automated Git push
"""

import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv

# Add the current directory to path so we can import multi_agent
import sys
sys.path.append(str(Path(__file__).parent))

from multi_agent import run_multi_agent

# Load environment variables
load_dotenv()

async def demo_multi_agent_workflow():
    """Demonstrate the complete multi-agent workflow."""
    
    print("🚀 Multi-Agent System Demo")
    print("=" * 60)
    print("This demo will:")
    print("1. Create a conversation between 3 agents")
    print("2. Generate HTML code")
    print("3. Wait for user approval")
    print("4. Automatically save and push to Git")
    print("=" * 60)
    
    # Demo request
    request = "Create a simple todo list web application with add/remove functionality"
    print(f"🎯 Request: {request}")
    print("-" * 60)
    
    try:
        # Run the multi-agent system
        responses = await run_multi_agent(request)
        
        print(f"\n✅ Demo completed! Total responses: {len(responses)}")
        print("\n📋 Summary of what happened:")
        
        business_analyst_count = 0
        software_engineer_count = 0
        product_owner_count = 0
        system_count = 0
        
        for response in responses:
            agent = response.get('agent', 'Unknown')
            if agent == 'BusinessAnalyst':
                business_analyst_count += 1
            elif agent == 'SoftwareEngineer':
                software_engineer_count += 1
            elif agent == 'ProductOwner':
                product_owner_count += 1
            elif agent == 'System':
                system_count += 1
        
        print(f"  👔 Business Analyst responses: {business_analyst_count}")
        print(f"  👨‍💻 Software Engineer responses: {software_engineer_count}")
        print(f"  👨‍💼 Product Owner responses: {product_owner_count}")
        print(f"  🤖 System messages: {system_count}")
        
        # Show the last few messages to see the outcome
        print("\n📄 Last few messages:")
        for response in responses[-3:]:
            agent = response.get('agent', 'Unknown')
            content = response.get('content', 'No content')
            print(f"  {agent}: {content[:100]}..." if len(content) > 100 else f"  {agent}: {content}")
            
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()

async def simulate_user_approval():
    """Simulate user approval to test the full workflow."""
    
    print("\n🔄 Simulating User Approval Workflow")
    print("=" * 60)
    
    # This would simulate a user typing "APPROVED" after reviewing the code
    print("In a real scenario, after the agents finish their conversation,")
    print("the user would review the HTML code and type 'APPROVED' to trigger")
    print("the automated Git push workflow.")
    print()
    print("The system would then:")
    print("1. Extract HTML from conversation history")
    print("2. Save to index.html")
    print("3. Run git commands to push to repository")
    print("4. Confirm successful deployment")

if __name__ == "__main__":
    print("🎭 Multi-Agent System Challenge Implementation")
    print("=" * 60)
    print("This implementation includes:")
    print("✅ Business Analyst Agent - Requirements and planning")
    print("✅ Software Engineer Agent - HTML/JavaScript development") 
    print("✅ Product Owner Agent - Quality assurance and approval")
    print("✅ Approval Termination Strategy - Detects 'APPROVED' signal")
    print("✅ HTML Code Extraction - Parses ```html blocks")
    print("✅ Automated Git Push - Stages, commits, and pushes code")
    print("=" * 60)
    
    # Run the demo
    asyncio.run(demo_multi_agent_workflow())
    
    # Show approval simulation
    asyncio.run(simulate_user_approval())
