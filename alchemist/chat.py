from langchain.schema import HumanMessage,  AIMessage
import json

def chat(agent, human_input):
    res = agent(human_input)
    try:
        tool = res["intermediate_steps"][0][0].tool
    except Exception as e:
        tool = None

    if tool is None:
        return res["output"], None, []

    enhanced_context = res["intermediate_steps"][0][1]
    enhance_agent_context(agent, enhanced_context)
    return enhanced_context, None, create_products(enhanced_context)

def enhance_agent_context(agent, enhanced_context):
    agent.memory.chat_memory.messages[-1].content = enhanced_context

def create_products(enhanced_context):
    ### IMPLEMENT LATER
    return enhanced_context
