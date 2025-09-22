from langchain_core.tools import tool
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langgraph.prebuilt import create_react_agent


@tool(description="Add two numbers and return the sum.")
def addTwoNum(a:int,b:int)->int:
 return a+b


tools=[addTwoNum]

load_dotenv()

api_key=os.getenv("GOOGLE_API_KEY")
print("API Key Loaded:", os.getenv("GOOGLE_API_KEY"))

llm_flash = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", api_key=api_key)

react_agent = create_react_agent(llm_flash, tools)
print("=== ReAct Agent (Gemini) ===")
# for event in react_agent.stream({"messages": [("user", "What is 12 + 8?")]}):
#     print(event)
# print("\n")

from langchain_core.messages import HumanMessage

inputs = {"messages": [HumanMessage(content="What is 12 + 8?")]}

# stream_mode can be "values" (final state snapshots) or "updates" (node-by-node)
for event in react_agent.stream(inputs, stream_mode="values"):
    # event is the latest state; print the last message
    print(event["messages"][-1].content)

