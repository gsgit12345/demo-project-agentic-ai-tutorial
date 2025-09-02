from langchain_google_genai import GoogleGenerativeAI  #  model connector and you can found it in lll sdk 


import os
from langchain_google_genai import GoogleGenerativeAI
from langgraph.graph import StateGraph, END

# --- Set API key ---
os.environ["GOOGLE_API_KEY"] = "your_google_api_key_here"

# --- Initialize Gemini LLM ---
llm = GoogleGenerativeAI(model="gemini-1.5-flash")

# --- Define State ---
class State(dict):
    question: str
    answer: str

# --- Define Node ---
def llm_node(state: State):
    response = llm.invoke(state["question"])
    return {"answer": response}

# --- Build Graph ---
graph = StateGraph(State)
graph.add_node("ask_gemini", llm_node)
graph.set_entry_point("ask_gemini")
graph.add_edge("ask_gemini", END)

# --- Compile Graph ---
app = graph.compile()

# --- Run Graph ---
result = app.invoke({"question": "Explain why Kubernetes and Hugging Face are different."})
print("Gemini Answer:", result["answer"])