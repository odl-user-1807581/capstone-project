import os
import asyncio
import re
import subprocess
from pathlib import Path
from dotenv import load_dotenv

from semantic_kernel.agents import AgentGroupChat, ChatCompletionAgent
from semantic_kernel.agents.strategies.termination.termination_strategy import TerminationStrategy
from semantic_kernel.agents.strategies.selection.kernel_function_selection_strategy import (
    KernelFunctionSelectionStrategy,
)
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior
from semantic_kernel.connectors.ai.open_ai.services.azure_chat_completion import AzureChatCompletion
from semantic_kernel.contents.chat_message_content import ChatMessageContent
from semantic_kernel.contents.utils.author_role import AuthorRole
from semantic_kernel.kernel import Kernel

# Load environment variables
load_dotenv()

class ApprovalTerminationStrategy(TerminationStrategy):
    """A strategy for determining when an agent should terminate."""
 
    async def should_agent_terminate(self, agent, history):
        """Check if the agent should terminate based on 'APPROVED' or 'READY FOR USER APPROVAL' in chat history."""
        # Check the last few messages in the chat history for approval signals
        for message in history[-10:]:  # Check last 10 messages
            if hasattr(message, 'content') and message.content:
                content_upper = message.content.upper()
                if "APPROVED" in content_upper or "READY FOR USER APPROVAL" in content_upper:
                    return True
        return False

def create_kernel():
    """Create and configure a Semantic Kernel instance."""
    kernel = Kernel()
    
    # Add Azure OpenAI Chat Completion service
    # Extract the base endpoint (remove deployment-specific parts)
    full_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    # For Azure OpenAI, we need: https://{resource}.openai.azure.com/
    if "openai.azure.com" in full_endpoint:
        # Extract just the base endpoint
        base_endpoint = full_endpoint.split("/openai/deployments")[0]
    else:
        base_endpoint = full_endpoint
    
    kernel.add_service(
        AzureChatCompletion(
            deployment_name=os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"),
            endpoint=base_endpoint,
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        )
    )
    
    return kernel

def extract_html_from_history(history):
    """Extract HTML code from chat history."""
    html_pattern = r'```html\s*(.*?)\s*```'
    
    for message in reversed(history):  # Start from the most recent messages
        if hasattr(message, 'content') and message.content:
            matches = re.findall(html_pattern, message.content, re.DOTALL | re.IGNORECASE)
            if matches:
                return matches[-1].strip()  # Return the last HTML block found
    
    return None

def save_html_to_file(html_content, filename="index.html"):
    """Save HTML content to a file."""
    try:
        # Save in the current directory (UI directory)
        filepath = Path(filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"HTML saved to {filepath.absolute()}")
        return str(filepath.absolute())
    except Exception as e:
        print(f"Error saving HTML file: {e}")
        return None

def create_git_script():
    """Create a bash script for Git operations."""
    script_content = '''#!/bin/bash
# Git push script
git add .
git commit -m "Auto-commit: HTML code approved and deployed"
git push origin feature/jk
echo "Code pushed to GitHub successfully!"
'''
    
    script_path = Path("push_to_github.sh")
    try:
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        # Make script executable on Unix-like systems
        if os.name != 'nt':  # Not Windows
            os.chmod(script_path, 0o755)
        
        return str(script_path.absolute())
    except Exception as e:
        print(f"Error creating Git script: {e}")
        return None

def execute_git_push():
    """Execute Git push using subprocess."""
    try:
        # For Windows, use PowerShell to execute git commands
        if os.name == 'nt':  # Windows
            commands = [
                "git add .",
                "git commit -m \"Auto-commit: HTML code approved and deployed\"",
                "git push origin feature/jk"
            ]
            
            git_success = True
            for cmd in commands:
                result = subprocess.run(
                    ["powershell", "-Command", cmd],
                    capture_output=True,
                    text=True,
                    shell=True
                )
                print(f"Executed: {cmd}")
                if result.returncode != 0:
                    print(f"Warning: {cmd} returned code {result.returncode}")
                    print(f"Error: {result.stderr}")
                    if "push" in cmd:
                        print("Note: Git push failed - this may be due to authentication. Files are still saved locally.")
                        git_success = False
                else:
                    print(f"Output: {result.stdout}")
        else:
            # Unix-like systems
            script_path = create_git_script()
            if script_path:
                result = subprocess.run(["bash", script_path], capture_output=True, text=True)
                print(f"Git script output: {result.stdout}")
                if result.stderr:
                    print(f"Git script errors: {result.stderr}")
                    git_success = False
                else:
                    git_success = True
        
        print("Git automation completed!")
        return git_success
        
    except Exception as e:
        print(f"Error executing Git operations: {e}")
        return False

async def run_multi_agent(input: str):
    """Implement the multi-agent system."""
    
    # Create kernel for all agents
    kernel = create_kernel()
    
    # Define personas and create agents
    business_analyst_instructions = """
You are a Business Analyst which will take the requirements from the user (also known as a 'customer') and create a project plan for creating the requested app. The Business Analyst understands the user requirements and creates detailed documents with requirements and costing. The documents should be usable by the SoftwareEngineer as a reference for implementing the required features, and by the Product Owner for reference to determine if the application delivered by the Software Engineer meets all of the user's requirements.
"""

    software_engineer_instructions = """
You are a Software Engineer, and your goal is create a web app using HTML and JavaScript by taking into consideration all the requirements given by the Business Analyst. The application should implement all the requested features. Deliver the code to the Product Owner for review when completed. You can also ask questions of the BusinessAnalyst to clarify any requirements that are unclear.
"""

    product_owner_instructions = """
You are the Product Owner which will review the software engineer's code to ensure all user requirements are completed. You are the guardian of quality, ensuring the final product meets all specifications. IMPORTANT: Verify that the Software Engineer has shared the HTML code using the format ```html [code] ```. This format is required for the code to be saved and pushed to GitHub. Once all client requirements are completed and the code is properly formatted, reply with 'READY FOR USER APPROVAL'. If there are missing features or formatting issues, you will need to send a request back to the SoftwareEngineer or BusinessAnalyst with details of the defect.
"""

    # Create ChatCompletionAgent instances
    business_analyst = ChatCompletionAgent(
        kernel=kernel,
        name="BusinessAnalyst",
        instructions=business_analyst_instructions,
    )

    software_engineer = ChatCompletionAgent(
        kernel=kernel,
        name="SoftwareEngineer",
        instructions=software_engineer_instructions,
    )

    product_owner = ChatCompletionAgent(
        kernel=kernel, 
        name="ProductOwner",
        instructions=product_owner_instructions,
    )

    # Create execution settings with termination strategy
    termination_strategy = ApprovalTerminationStrategy()

    # Create AgentGroupChat
    group_chat = AgentGroupChat(
        agents=[business_analyst, software_engineer, product_owner],
        termination_strategy=termination_strategy
    )

    # Add the user input to start the conversation
    await group_chat.add_chat_message(
        ChatMessageContent(role=AuthorRole.USER, content=input)
    )

    # Run the conversation
    responses = []
    
    async for response in group_chat.invoke():
        # Handle different response types from semantic-kernel
        if hasattr(response, 'message'):
            agent_name = response.message.name if hasattr(response.message, 'name') else "System"
            content = response.message.content if hasattr(response.message, 'content') else str(response.message)
        else:
            agent_name = response.name if hasattr(response, 'name') else "System"
            content = response.content if hasattr(response, 'content') else str(response)
        
        responses.append({
            "agent": agent_name,
            "content": content
        })
        
        # Check if we should terminate and handle approval
        if await termination_strategy.should_agent_terminate(None, group_chat.history):
            print("APPROVED detected! Starting automated Git push...")
            
            # Extract HTML from chat history
            html_content = extract_html_from_history(group_chat.history)
            
            if html_content:
                # Save HTML to file
                saved_file = save_html_to_file(html_content)
                
                if saved_file:
                    # Execute Git push
                    git_success = execute_git_push()
                    
                    if git_success:
                        responses.append({
                            "agent": "System",
                            "content": f"✅ Code approved and successfully pushed to GitHub! HTML saved as {saved_file}"
                        })
                    else:
                        responses.append({
                            "agent": "System",
                            "content": f"✅ Code approved and saved locally! HTML saved as {saved_file}. Note: Git push may have failed due to permissions."
                        })
                else:
                    responses.append({
                        "agent": "System", 
                        "content": "❌ Failed to save HTML file"
                    })
            else:
                responses.append({
                    "agent": "System",
                    "content": "❌ No HTML code found in conversation history"
                })
            
            break
    
    return responses