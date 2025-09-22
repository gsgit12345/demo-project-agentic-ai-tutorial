from langchain_google_genai import GoogleGenerativeAI  #  model connector and you can found it in lll sdk 


import os
from langchain_google_genai import GoogleGenerativeAI
from langgraph.graph import StateGraph, END
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
print("API Key Loaded:", os.getenv("GOOGLE_API_KEY"))

# Initialize Gemini LLM (LangChain connector)
llm = GoogleGenerativeAI(model="gemini-1.5-flash")

# Send a prompt
response = llm.invoke("Write a 3-line motivational quote about AI and learning.")
print(response)


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