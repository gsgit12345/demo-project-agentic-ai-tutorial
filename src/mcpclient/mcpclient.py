import asyncio
import os
from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.graph import StateGraph, MessagesState, START
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage


load_dotenv()
print("API Key Loaded:", os.getenv("GOOGLE_API_KEY"))

async def main():
    google_api = os.getenv("GOOGLE_API_KEY")
    weather_key = os.getenv("OWM_API_KEY")

    if not google_api:
        raise ValueError("google api key is not available")
    if not weather_key:
        raise ValueError("weather api key is not available")

    # Start MCP client
    client = MultiServerMCPClient(
        {
            "weather": {
                "transport": "stdio",
                "command": "/home/iid/agenticai/demo-project-agentic-ai-tutorial/src/mcpserver/mcp-openweather/mcp-weather",
                "args": [],
                "env": {"OWM_API_KEY": weather_key},
            }
        }
    )

    tools = await client.get_tools()

    # Gemini LLM
    llm = GoogleGenerativeAI(model="gemini-1.5-flash")

    # ---- FIXED call_model ----
    def call_model(state: MessagesState):
        user_message = state["messages"][-1].content
        tool_descriptions = "\n".join([str(tool) for tool in tools])

        prompt = f"""
        You are a helpful assistant. 
        You have access to the following tools:
        {tool_descriptions}

        User query: {user_message}
        """

        response = llm.invoke(prompt)

        return {"messages": state["messages"] + [AIMessage(content=str(response))]}

    # Build LangGraph workflow
    builder = StateGraph(MessagesState)
    builder.add_node("call_model", call_model)
    builder.add_node("tools", ToolNode(tools))

    builder.add_edge(START, "call_model")
    builder.add_conditional_edges("call_model", tools_condition)
    builder.add_edge("tools", "call_model")

    graph = builder.compile()

    print("\n--- Weather Query ---")
    result = await graph.ainvoke({
        "messages": [HumanMessage(content="what is weather in delhi today?")]
    })

    print(result["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())
