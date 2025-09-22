import os
from openai import OpenAI
from dotenv import load_dotenv
from agents import Agent, Runner, SQLiteSession
import asyncio

load_dotenv()

async def main():
    agent = Agent(name="Assistant", instructions="Reply concisely.")
    
    session = SQLiteSession("conversation_123", "conversation_history.db")

    result1 = await Runner.run(agent, "What city is the Golden temple in?", session=session)
    print(result1.final_output)

    result2 = await Runner.run(agent, "What state is it in?", session=session)
    print(result2.final_output)  

    result3 = await Runner.run(agent, "and Country?", session=session)
    print(result3.final_output)  


if __name__ == "__main__":
    asyncio.run(main())