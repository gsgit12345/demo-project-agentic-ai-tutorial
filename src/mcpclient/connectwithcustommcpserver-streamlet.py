import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
import streamlit as st

load_dotenv()

async def run_mcp_query(user_input):
    print("API Key Loaded:", os.getenv("GOOGLE_API_KEY"))

    # Initialize Gemini LLM (LangChain connector)
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )

    # Send a prompt
    #response = llm.invoke("Write a 3-line motivational quote about AI and learning.")
    #print(response)

    # setup the mcp client connecting to the mcp server 
    # client = MultiServerMCPClient(
    #     {
    #         "Math": {
    #             "command": "python",
    #             "args": ["/home/iid/agenticai/demo-project-agentic-ai-tutorial/src/custommcpserver/custom_mcpserver.py"],
    #             "transport": "stdio",
    #         }
    #     }
    # )
    client = MultiServerMCPClient(
        {
            "math": {
                "transport": "streamable_http",
                "url": "http://127.0.0.1:8000/mcp"  # URL of your MCP server
            }
        }
    )    
    


    # this must stay inside async function
    tools = await client.get_tools()
    #print("Available tools:", tools)
    
    model_with_tools = llm.bind_tools(tools)  # binding the tool with model 
    #print(model_with_tools)
    
    tool_node = ToolNode(tools)  # creating the tool node .wrapping the all tool into node
    
    def should_continue(state: MessagesState):
        messages = state["messages"]  #list of message .basically this is the memory 
        last_message = messages[-1]  # last message in the list of message
        if last_message.tool_calls:  # checking that in message there is any message is specifed or not
            return "tools"   # this is the custom function
        return END

    async def call_model(state: MessagesState):   # this function is generatiing the response for user message
                                                  #it will take the user message and call the model and generate the response  
        messages = state["messages"]
        response = await model_with_tools.ainvoke(messages) # model will check that we need to invoke the tool or not
            # Debug: show what Gemini actually returned
        print("\n--- DEBUG RESPONSE ---")
        print(response)
        print("----------------------\n")

        return {"messages": [response]}
    
    builder = StateGraph(MessagesState)  # started creating the flow 
    
    builder.add_node("call_model", call_model)  #this is  adding the node in stategraph and binding the call_model() function
    
    builder.add_node("tools", tool_node)


    builder.add_edge(START, "call_model") #defining the connection between tool
    
    builder.add_conditional_edges(    
        "call_model",
        should_continue,   # here it is decided that we need the tool.means llm needs the tool or not 
    )
    builder.add_edge("tools", "call_model")  # at the last flow will come to the call_model()

        # Compile the graph
    graph = builder.compile()

# Note:--All code is copy and paste from the connectwithcustommcpserver.py except below code
# here we are writing the code for stream let 
    result = await graph.ainvoke({"messages": [{"role": "user", "content": user_input}]})


    print("Answer:", result["messages"][-1].content)


    last_message=result["messages"][-1].content
    return last_message if isinstance(last_message, str) else str(last_message)



def main():
    st.set_page_config(page_title="MCP Math Chat", page_icon="🧮")
    st.title("🧮 MCP Math Chat (Streamlit)")

    user_input = st.text_input("Ask me something math-related:")
    if st.button("Send") and user_input.strip():
        with st.spinner("Thinking..."):
            answer = asyncio.run(run_mcp_query(user_input))
            st.success(answer)



if __name__ == "__main__":
     main()

# flow of the code  

# You’ve built a mini-agent pipeline using:

# MCP client for tool discovery,

# LangChain + LangGraph for orchestration,

# Gemini LLM for reasoning,

# Custom MCP math server for actual execution.

# This is the core of Agentic AI:
# 👉 LLM does reasoning → decides tool → calls tool → uses result → answers user.