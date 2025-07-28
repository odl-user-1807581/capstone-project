import asyncio
from multi_agent import run_multi_agent

async def test():
    responses = await run_multi_agent('Create a simple contact form with name and email fields')
    print(f'Total responses: {len(responses)}')
    for i, r in enumerate(responses[-3:]):
        agent = r.get("agent", "Unknown")
        content = r.get("content", "")
        print(f'{i}: {agent}: {content[:200]}...')

if __name__ == "__main__":
    asyncio.run(test())
