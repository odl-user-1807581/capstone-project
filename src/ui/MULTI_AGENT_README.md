# Multi-Agent System Implementation

This implementation creates a Multi-Agent System with three specialized agents:

## Agents

### 1. Business Analyst Agent
- **Name**: BusinessAnalyst
- **Role**: Takes user requirements and creates detailed project plans and specifications
- **Output**: Detailed requirements and costing documents for the Software Engineer

### 2. Software Engineer Agent  
- **Name**: SoftwareEngineer
- **Role**: Creates web applications using HTML and JavaScript based on Business Analyst requirements
- **Output**: Complete HTML/JavaScript code in proper format (```html [code] ```)

### 3. Product Owner Agent
- **Name**: ProductOwner  
- **Role**: Reviews code quality and ensures all requirements are met
- **Output**: Quality assessment and "READY FOR USER APPROVAL" when complete

## Automation Features

### Termination Strategy
The system uses `ApprovalTerminationStrategy` which terminates when:
- User sends "APPROVED" in the chat history
- Automatically triggers Git automation workflow

### Git Automation
When "APPROVED" is detected:
1. Extracts HTML code from chat history using regex pattern ````html ... ```
2. Saves code to `index.html` file
3. Creates and executes Git commands to:
   - Stage changes (`git add .`)
   - Commit with message ("Auto-commit: HTML code approved and deployed")
   - Push to main branch (`git push origin main`)

## Usage

```python
from multi_agent import run_multi_agent

# Run the multi-agent system
responses = await run_multi_agent("Create a simple todo list web app")

# User approves by sending "APPROVED"
# System automatically saves HTML and pushes to Git
```

## Environment Variables Required

```
AZURE_OPENAI_CHAT_DEPLOYMENT_NAME=gpt-4o
AZURE_OPENAI_ENDPOINT=https://your-endpoint.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2025-01-01-preview
AZURE_OPENAI_API_KEY=your-api-key
```

## File Structure

```
src/ui/
├── multi_agent.py          # Main multi-agent implementation
├── app.py                  # Streamlit UI integration
├── .env                    # Environment variables
├── requirements.txt        # Python dependencies
└── index.html              # Generated HTML (after approval)
```
