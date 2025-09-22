#!pip install langgraph-supervisor langchain-openai

from langchain_openai import ChatOpenAI

from langgraph_supervisor import create_supervisor
from langgraph.prebuilt import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools import DuckDuckGoSearchRun
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.tools import tool

from dotenv import load_dotenv
import os

# Initialize OpenAI model
load_dotenv()

api_key=os.getenv("GOOGLE_API_KEY")
print("API Key Loaded:", os.getenv("GOOGLE_API_KEY"))

model = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", api_key=api_key)

msg=model.invoke('hello').content

print(msg)
def search_duckduckgo(query: str):
    """Searches DuckDuckGo using LangChain's DuckDuckGoSearchRun tool."""
    search = DuckDuckGoSearchRun()
    return search.invoke(query)

@tool(description="Add two numbers and return the sum.")
def add(a: float, b: float) -> float:
    """Add two numbers."""
    return a + b

@tool(description="Add two numbers and return the sum.")
def multiply(a: float, b: float) -> float:
    """Multiply two numbers."""
    return a * b

math_agent = create_react_agent(
    model=model,
    tools=[add, multiply],
    name="math_expert",
    prompt="You are a math expert. Always use one tool at a time."
)

research_agent = create_react_agent(
    model=model,
    tools=[search_duckduckgo],
    name="research_expert",
    prompt="You are a world class researcher with access to web search. Do not do any math."
)
workflow = create_supervisor(
    [research_agent, math_agent],
    model=model,
    prompt=(
        "You are a team supervisor managing a research expert and a math expert. "
        "For current events, use research_agent. "
        "For math problems, use math_agent."
    )
)


# Create supervisor workflow
workflow = create_supervisor(
    [research_agent, math_agent],
    model=model,
    prompt=(
        "You are a team supervisor managing a research expert and a math expert. "
        "For current events, use research_agent. "
        "For math problems, use math_agent."
    )
)
# Compile and run
app = workflow.compile()

result = app.invoke({
    "messages": [
        {
            "role": "user",
            "content": "what is quantum computing?"
        }
    ]
})

print(result)
for m in result["messages"]:
    m.pretty_print()


print("  next  section  =======================================================================")


# Compile and run
app = workflow.compile()
result = app.invoke({
    "messages": [
        {
            "role": "user",
            "content": "what is the weather in delhi today. Multiply it by 2 and add 5"
        }
    ]
})

for m in result["messages"]:
    m.pretty_print()
