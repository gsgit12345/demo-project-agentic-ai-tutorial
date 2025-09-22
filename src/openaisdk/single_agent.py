import os
from openai import OpenAI
from dotenv import load_dotenv
from agents import Agent, Runner
import tiktoken  # make sure to install with `pip install tiktoken`


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

response = client.chat.completions.create(
    model="gpt-3.5-turbo", 
    messages=[
        {"role": "system", "content": agent.instructions},  # use agent's instructions
        {"role": "user", "content": prompt}
    ],
    max_tokens=2   # limit to 2 tokens
)

# Print final output
print(response.choices[0].message.content)

# counting the token 

encoding = tiktoken.encoding_for_model("gpt-5-mini")  

# Count tokens in instructions
instr_tokens = len(encoding.encode(agent.instructions))

# Count tokens in prompt
prompt_tokens = len(encoding.encode(prompt))

# Count tokens in model output
output_tokens = len(encoding.encode(result.final_output))

total_tokens = instr_tokens + prompt_tokens + output_tokens

print(f"Tokens used:")
print(f" - Instructions: {instr_tokens}")
print(f" - Prompt: {prompt_tokens}")
print(f" - Output: {output_tokens}")
print(f" - Total: {total_tokens}")
