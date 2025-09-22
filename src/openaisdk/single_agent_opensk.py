import os
from openai import OpenAI
from dotenv import load_dotenv
from agents import Agent, Runner


# Load environment variables
load_dotenv()

# Initialize agent
agent = Agent(name="Assistant", instructions="hi")

# Minimal prompt
prompt = "Hi"

# Run agent with token limit
# Note: openai-agents does not always expose max_tokens directly,
# but most versions allow passing **client or options**. 
# We'll use OpenAI client with max_tokens=2.
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

result = Runner.run_sync(agent, prompt)

print(result.final_output)
