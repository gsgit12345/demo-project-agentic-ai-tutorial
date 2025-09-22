import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, START, END

# Load your API key
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", api_key=api_key)

# Define Agents (functions that use LLM)
def research_agent(state: dict):
    query = state["query"]
    response = llm.invoke(f"Find information about: {query}")
    return {"research": response.content}

def summarizer_agent(state: dict):
    research = state["research"]
    response = llm.invoke(f"Summarize this in 3 lines:\n{research}")
    return {"summary": response.content}

# Build Multi-Agent Graph
graph = StateGraph(dict)

graph.add_node("research", research_agent)
graph.add_node("summarizer", summarizer_agent)

graph.add_edge(START, "research")
graph.add_edge("research", "summarizer")
graph.add_edge("summarizer", END)

multiagent = graph.compile()

# Run
result = multiagent.invoke({"query": "Shore Temple in Mahabalipuram"})
print("📌 Final Summary:", result["summary"])