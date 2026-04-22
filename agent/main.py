import asyncio
import os
from agents import Agent, Runner
from tools import list_repo_contents, suggest_plan

agent = Agent(
    name="Repo Assistant",
    instructions="""
You are a careful AI repo assistant.

Your job:
- chat with the user about this repository
- explain what is in the repository
- help plan the next coding steps
- use tools when helpful
- never claim you changed files unless a real tool did it
- keep answers practical and clear
""",
    tools=[list_repo_contents, suggest_plan],
)

async def main():
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY is not set in this Codespace.")

    print("Repo Assistant is ready. Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in {"exit", "quit"}:
            break

        result = await Runner.run(agent, user_input)
        print(f"\nAgent: {result.final_output}\n")

if __name__ == "__main__":
    asyncio.run(main())