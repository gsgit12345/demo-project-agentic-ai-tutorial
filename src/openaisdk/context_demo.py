import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

import asyncio
from dataclasses import dataclass

from agents import Agent, Runner, function_tool, RunContextWrapper


@dataclass
class UserInfo:  
    name: str
    uid: int
    last_purchase: str



@function_tool  
async def fetch_user_purchase(wrapper: RunContextWrapper[UserInfo]) -> str:  
    """Fetch the last item the user purchased. Call this function to get user's purchase history."""
    return f"The user {wrapper.context.name} recently purchased a {wrapper.context.last_purchase}."



async def main():
    # Context instance passed to the agent
    user_info = UserInfo(name="Aarohi", uid=123, last_purchase="laptop")

    agent = Agent[UserInfo](  
        name="Assistant",
        instructions="You are a helpful assistant. Use tools if needed.",
        tools=[fetch_user_purchase],
    )

    result = await Runner.run(  
        starting_agent=agent,
        input="What did the user recently purchase?",
        context=user_info,
    )    

    print("\n=== Final Output ===")
    print(result.final_output)      

if __name__ == "__main__":
    asyncio.run(main())