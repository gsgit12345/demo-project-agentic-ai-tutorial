from agents import GuardrailFunctionOutput, Agent, Runner
from pydantic import BaseModel
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from agents import Agent, InputGuardrail, GuardrailFunctionOutput, Runner
from agents.exceptions import InputGuardrailTripwireTriggered
from pydantic import BaseModel
import asyncio



class HomeworkOutput(BaseModel):
    is_homework: bool
    reasoning: str

'''
{
  "is_homework": true,
  "reasoning": "The user asked about solving a math problem, which is clearly homework."
}
'''

guardrail_agent = Agent(
    name="Guardrail check",
    instructions="Check if the user is asking about homework.",
    output_type=HomeworkOutput,
)



history_agent = Agent(
    name="History Agent",
    handoff_description="Specialist agent for historical questions",
    instructions="You provide assistance with historical queries. Explain important events and context clearly.",
)

math_agent = Agent(
    name="Math Agent",
    handoff_description="Specialist agent for math questions",
    instructions="You provide help with math problems. Explain your reasoning at each step and include examples",

)



async def homework_guardrail(ctx, agent, input_data):
    result = await Runner.run(guardrail_agent, input_data, context=ctx.context)
    final_output = result.final_output_as(HomeworkOutput)
    return GuardrailFunctionOutput(
        output_info=final_output,
        tripwire_triggered=not final_output.is_homework,
    )


allocator_agent = Agent(
    name="Allocator Agent",
    instructions="You determine which agent to use based on the user's homework question",
    handoffs=[history_agent, math_agent],
        input_guardrails=[
        InputGuardrail(guardrail_function=homework_guardrail),
    ]
)


async def main():
    result = await Runner.run(allocator_agent, "who was the first prime minister of India?")
    print(result.final_output)


    try:
        result = await Runner.run(allocator_agent, "What is the meaning of life?")
        print(result.final_output)
    except InputGuardrailTripwireTriggered as e:
        print("Guardrail blocked this input:", e)


if __name__ == "__main__":
    asyncio.run(main())