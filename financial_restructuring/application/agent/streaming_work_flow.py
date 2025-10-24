# graph_definition.py
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from financial_restructuring.domian.constants.domain_constants import OpenAiModels
from typing import TypedDict, Any
import json
from .agents import router_agent, optimizer_agent, welcome_agent, fallback_agent, humanizer_agent, extracter_agent
from .tools import generate_optimized_plan, get_user_information
from .prompts import ROUTER_SYSTEM_INST, WELCOME_SYSTEM_INST, FALLBACK_SYSTEM_INST, HUMANIZER_SYST_INST, EXTRACTER_SYSTEM_INST

class State(TypedDict):
    user_input: str
    llm_input: str
    llm_output: str
    user_id: str
    tool_1_output: Any
    tool_2_output: Any
    stream_output: Any
    route: str

llm = ChatOpenAI(model=OpenAiModels.GPT_MINI.value, temperature=0)

graph = StateGraph(State)

def router_node(state: State):
    messages = [
        {"role": "system", "content": ROUTER_SYSTEM_INST},
        {"role": "user", "content": state["user_input"]}
    ]
    state["route"] = router_agent.invoke(messages).content
    print(f"Selected route", state["route"])
    return state

def optimizer_plan_node(state: State):

    messages = [
        {"role": "system", "content": EXTRACTER_SYSTEM_INST},
        {"role": "user", "content": state["user_input"]}
    ]

    state["user_id"] = extracter_agent.invoke(messages).content
    print("User id => ", state["user_id"])
    state["tool_1_output"] = get_user_information(state["user_id"])
    state["tool_2_output"] = generate_optimized_plan(state["tool_1_output"])
    print("Tool 1 output", state["tool_2_output"])
    return state

def welcome_node(state: State):
    messages = [
        {"role": "system", "content": WELCOME_SYSTEM_INST},
        {"role": "user", "content": state["user_input"]}
    ]

    def stream():
        for chunk in fallback_agent.stream(messages):
            if chunk.content:
                yield chunk.content

    state["stream_output"] = stream()
    return state

def fallback_node(state: State):

    messages = [
        {"role": "system", "content": FALLBACK_SYSTEM_INST},
        {"role": "user", "content": state["user_input"]}
    ]

    def stream():
        for chunk in fallback_agent.stream(messages):
            if chunk.content:
                yield chunk.content

    state["stream_output"] = stream()
    return state

def humanizer_node(state: State):

    messages = [
        {"role": "system", "content": HUMANIZER_SYST_INST},
        {"role": "user", "content": json.dumps(state["tool_2_output"])}
    ]

    def stream():
        for chunk in humanizer_agent.stream(messages):
            if chunk.content:
                yield chunk.content

    state["stream_output"] = stream()
    return state

graph.add_node("router", router_node)
graph.add_node("optimizer_plan", optimizer_plan_node)
graph.add_node("welcome", welcome_node)
graph.add_node("fallback", fallback_node)
graph.add_node("humanizer", humanizer_node)
graph.add_node("end", lambda s: s)

graph.set_entry_point("router")

graph.add_conditional_edges(
    "router",
    lambda state: state["route"],
    {
        "optimizer_plan": "optimizer_plan",
        "welcome": "welcome",
        "fallback": "fallback"
    }
)

graph.add_edge("optimizer_plan", "humanizer")
graph.add_edge("humanizer", "end")
graph.add_edge("welcome", "end")
graph.add_edge("fallback", "end")

streaming_agent_graph = graph.compile()
