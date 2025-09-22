import asyncio
import os
import json
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
        raise ValueError("Google API key is not available")
    if not weather_key:
        raise ValueError("Weather API key is not available")

    # Initialize MCP client for weather and calculator
    client = MultiServerMCPClient(
        {
            "weather": {
                "transport": "stdio",
                "command": "/home/iid/agenticai/demo-project-agentic-ai-tutorial/src/mcpserver/mcp-openweather/mcp-weather",
                "args": [],
                "env": {"OWM_API_KEY": weather_key},
            },
            "calculator": {
                "transport": "stdio",
                "command": "python",
                "args": ["-m", "mcp_server_calculator"],
            },
        }
    )

    # Fetch all tools
    tools_list = await client.get_tools()
    print("Available tools from MCP server:")
    for t in tools_list:
      print(f"Tool name: {t.name}, description: {t.description}")


    # Safe helper function to get a tool by name
    def get_tool_by_name(tools, name):
        for tool in tools:
            if tool.name == name:
                return tool
        return None

    weather_tool = get_tool_by_name(tools_list, "weather")
    calculator_tool = get_tool_by_name(tools_list, "calculate")

    if not weather_tool:
        raise RuntimeError("Weather tool not found from MCP server.")
    if not calculator_tool:
        raise RuntimeError("Calculator tool not found from MCP server.")

    # Initialize LLM
    llm = GoogleGenerativeAI(model="gemini-1.5-flash")

    # ---- Call model node ----
    async def call_model(state: MessagesState):
        user_message = state["messages"][-1].content.lower()

        # Weather query
        if "weather" in user_message:
            city = "Delhi"
            for word in state["messages"][-1].content.split():
                if word[0].isupper():
                    city = word
                    break

            tool_output = await client.invoke_tool(
                weather_tool, {"city": city, "lang": "en", "units": "c"}
            )

            result_json = {
                "status": "success",
                "data": {
                    "city": tool_output.get("city", city),
                    "temperature": tool_output.get("temperature"),
                    "condition": tool_output.get("condition"),
                    "humidity": tool_output.get("humidity")
                }
            }

            return {"messages": state["messages"] + [AIMessage(content=json.dumps(result_json))]}

        # Calculator query
        elif any(op in user_message for op in ["+", "-", "*", "/"]):
            tool_output = await client.invoke_tool(
                calculator_tool, {"expression": user_message}
            )
            return {"messages": state["messages"] + [AIMessage(content=str(tool_output.get("result")))]}

        # Fallback to LLM
        response = llm.invoke(state["messages"][-1].content)
        return {"messages": state["messages"] + [AIMessage(content=str(response))]}

    # Build LangGraph workflow
    builder = StateGraph(MessagesState)
    builder.add_node("call_model", call_model)
    builder.add_node("tools", ToolNode([]))  # Tools handled manually
    builder.add_edge(START, "call_model")
    builder.add_conditional_edges("call_model", tools_condition)
    builder.add_edge("tools", "call_model")
    graph = builder.compile()

    print("\n--- Weather & Calculator Agent ---")
    while True:
        user_question = input("\nAsk me anything (weather or calculation) → ")
        if user_question.strip().lower() in ["exit", "quit"]:
            print("Goodbye! 👋")
            break

        print("\n--- Agent is thinking... ---")
        result = await graph.ainvoke({"messages": [HumanMessage(content=user_question)]})
        print("\n--- Answer ---")
        print(result["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())
