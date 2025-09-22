from langchain_core.tools import tool
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langgraph.prebuilt import create_react_agent
from typing import TypedDict
from langchain_core.messages import HumanMessage

class CalcInput(TypedDict):
    a: int
    b: int

@tool(description="Add two numbers and return the sum.")
def add_numbers(inputs: CalcInput) -> int:
    return inputs["a"] + inputs["b"]

@tool(description="multiply two numbers and return the sum.")
def multiply_numbers(inputs: CalcInput) -> int:
    return inputs["a"] * inputs["b"]

# Tool 2: String manipulator

class StringInput(TypedDict):
    text: str

@tool(description="uppser case string")
def uppercase_text(inputs: StringInput) -> str:
    return inputs["text"].upper()

@tool(description="Add two numbers and return the sum.")
def addTwoNum(a:int,b:int)->int:
 return a+b


tools=[addTwoNum]

load_dotenv()

api_key=os.getenv("GOOGLE_API_KEY")
print("API Key Loaded:", os.getenv("GOOGLE_API_KEY"))

llm_flash = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", api_key=api_key)
tools = [add_numbers, multiply_numbers, uppercase_text]

agent = create_react_agent(llm_flash, tools)

response=agent.invoke({"messages":[HumanMessage(content="What is 12 + 8?")]})

print(response["messages"][-1].content)

response=agent.invoke({"messages":[HumanMessage(content="Multiply 7 and 6.")]

})

print(response["messages"][-1].content)

# ✅ So messages and content are part of the LangChain message object structure, not your own variables.

response=agent.invoke({"messages":[HumanMessage(content="convert hello in uppercase")]})

print(response["messages"][-1].content)

