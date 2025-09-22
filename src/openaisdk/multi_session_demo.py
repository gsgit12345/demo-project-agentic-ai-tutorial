import os
from openai import OpenAI
from dotenv import load_dotenv
from agents import Agent, Runner, SQLiteSession
import asyncio

load_dotenv()


async def main():
    # Create a single agent
    agent = Agent(
        name="Assistant",
        instructions="Reply concisely and clearly."
    )

    session_user1 = SQLiteSession("user_123", "multi_session_db.db")
    session_user2 = SQLiteSession("user_456", "multi_session_db.db")   

    print("=== User 1 Conversation ===")
    result1 = await Runner.run(
        agent,
        "Hi, what is the capital of India?",
        session=session_user1
    )
    print("User 1:", result1.final_output)  

    result2 = await Runner.run(
        agent,
        "And what about its population?",
        session=session_user1
    )
    print("User 1:", result2.final_output)  

    print("\n=== User 2 Conversation ===")
    result3 = await Runner.run(
        agent,
        "Hello! Who wrote Harry Potter?",
        session=session_user2
    )
    print("User 2:", result3.final_output)  


    result4 = await Runner.run(
        agent,
        "And when was it written?",
        session=session_user2
    )
    print("User 2:", result4.final_output)  # Agent remembers previous turn


if __name__ == "__main__":
    asyncio.run(main())