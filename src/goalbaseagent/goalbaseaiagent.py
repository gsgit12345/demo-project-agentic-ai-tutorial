from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, Tool, AgentType
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv
import os
import re
from langchain_ollama.llms import OllamaLLM


load_dotenv()


# llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)


# curl http://localhost:11434/api/generate -d '{
#   "model": "llama3.2",
#   "prompt": "Hello! How are you?"
# }'


# Initialize LLM
llm = LLM(
    model="ollama/llama3.2",
    base_url="http://localhost:11434"
)

response = llm.generate("Explain AI in one simple sentence.")

# Print response
print("Llama 3.2 says:", response)
