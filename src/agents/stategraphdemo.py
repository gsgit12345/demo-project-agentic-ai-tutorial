from IPython.display import Image,display
from langgraph.graph import StateGraph,START
from langchain_openai import ChatOpenAI
import requests
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import MessagesState

from langgraph.prebuilt import ToolNode, tools_condition
from langchain_community.tools import DuckDuckGoSearchRun
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langgraph.prebuilt import create_react_agent

from langchain_core.tools import tool


from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages

class State(TypedDict):
    messages: Annotated[list, add_messages]
     
#search = DuckDuckGoSearchRun()
#result = search.invoke("Obama's first name?")

# Print the results#
#print(result)

def search_duckduckgo(query: str):
    """Searches DuckDuckGo using LangChain's DuckDuckGoSearchRun tool."""
    search = DuckDuckGoSearchRun()
    return search.invoke(query)

# Example usage
result = search_duckduckgo("what are AI agent")
#print(result)
@tool(description="Add two numbers and return the sum.")

def multiply(a:int,b:int) -> int:
    """
    Multiply a and b
    """
    return a* b

@tool(description="Add two numbers and return the sum.")
def add(a:int,b:int) -> int:
    """
    Adds a and b
    """
    return a + b
load_dotenv()

api_key=os.getenv("GOOGLE_API_KEY")
print("API Key Loaded:", os.getenv("GOOGLE_API_KEY"))

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", api_key=api_key)

llm.invoke('hello').content
tools = [search_duckduckgo, add, multiply]

llm_with_tools = llm.bind_tools(tools)
     
def chatbot(state: State):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}


graph_builder = StateGraph(State)

# Define nodes
graph_builder.add_node("assistant",chatbot)
graph_builder.add_node("tools",ToolNode(tools))

#define edges
graph_builder.add_edge(START,"assistant")
graph_builder.add_conditional_edges("assistant",tools_condition)
graph_builder.add_edge("tools","assistant")

react_graph=graph_builder.compile()
display(Image(react_graph.get_graph().draw_mermaid_png()))
response = react_graph.invoke({"messages": [HumanMessage(content="what is the weather in delhi. Multiply it by 2 and add 5.")]})
#print(response["messages"])
last_msg = response["messages"][-1]

# Extract content (string) from the message
msg_text = last_msg.content if hasattr(last_msg, "content") else str(last_msg)

# Print only the first 100 characters
print(msg_text[:100])
