import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

import asyncio
from agents import Agent, Runner, WebSearchTool

agent = Agent(
    name="Assistant",
    instructions="Answer the question using real-time web search if needed.",
    tools=[
        WebSearchTool(),
    ],
)


async def main():
    # Ask the agent a question that needs real-time info
    result = await Runner.run(
        agent,
        input="What is the latest news about AI in 2025?"
    )

    # Print the agent's final answer
    print("Agent response:", result.final_output)

if __name__ == "__main__":
    asyncio.run(main())