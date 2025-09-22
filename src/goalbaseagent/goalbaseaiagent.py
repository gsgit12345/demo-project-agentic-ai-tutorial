#from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, Tool, AgentType
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv
from openai import OpenAI
from langchain_community.llms import Ollama
from langchain_ollama import OllamaLLM


import os

load_dotenv()

# Initialize LLM with langchain_community
llm = OllamaLLM(
    model="llama3.2",
    base_url="http://localhost:11434"
)

# Option 1: Using invoke (simpler for one-off prompt)
response = llm.invoke("Explain AI in one simple sentence.")
print("Llama 3.2 says:", response)
