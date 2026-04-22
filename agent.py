from agents import Agent, Runner
import asyncio
import os

agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant.",
    model="gpt-5.4-nano"
)

async def main():
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY is not set")
    result = await Runner.run(agent, "Say hello and explain what you can do.")
    print(result.final_output)

asyncio.run(main())
