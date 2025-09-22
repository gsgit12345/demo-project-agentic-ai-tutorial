from langchain.memory import ConversationBufferMemory
from pymongo import MongoClient
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client.agentic_ai
sessions = db.sessions

# Fetch session
session = sessions.find_one({"user_id": "123"})
messages = session['messages'] if session else []

# LangChain memory
memory = ConversationBufferMemory(memory_key="chat_history", input_key="input", chat_memory=messages)

# Agent
llm = ChatOpenAI(model_name="gpt-4")
chain = ConversationChain(llm=llm, memory=memory)

# User query
user_input = "What’s the weather in Hyderabad?"
response = chain.run(user_input)

# Update MongoDB
sessions.update_one(
    {"user_id": "123"},
    {"$set": {"messages": memory.chat_memory}},
    upsert=True
)


# ✅ Summary

# LangChain manages memory and agents.

# LangGraph orchestrates tools, agents, and retrieval.

# MongoDB stores session data persistently.

# Dynamic Context Builder pulls messages from MongoDB + tools for prompt creation.

# Agent executes and updates session back to MongoDB.