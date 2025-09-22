import os
from openai import OpenAI
from dotenv import load_dotenv
from agents import Agent
from agents import Runner


load_dotenv()

history_tutor_agent = Agent(
    name="History Agent",
    handoff_description="This is the agent which response the history related question",
    instructions="You provide The Answer with historical queries. Explain important events and context clearly.",
)

math_tutor_agent = Agent(
    name="Math Gent",
    handoff_description="This agent will give the answer of math related question",   # this is for other agent that this agent serve the question related to math
    instructions="You provide help with math questin. Explain your reasoning at each step and include examples",

)

allocator_agent = Agent(
    name="Task Allocator Agent",
    instructions="You determine which agent to use based on the user's homework question",
    handoffs=[history_tutor_agent, math_tutor_agent]      # this agent decide which agent serve the question.it pick the agent 
)


result = Runner.run_sync(allocator_agent, "What is the capital of India?")
print(result.final_output)