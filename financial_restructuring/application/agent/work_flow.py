# graph_definition.py
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI

from financial_restructuring.domian.constants.domain_constants import OpenAiModels
from langchain_google_genai import ChatGoogleGenerativeAI

from financial_restructuring.domian.constants.env_constants import GEMINI_API_KEY

from typing import TypedDict

class State(TypedDict):
    user_input: str
    llm_input: str
    llm_output: str

llm = ChatOpenAI(model=OpenAiModels.GPT_MINI.value, temperature=0)

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=GEMINI_API_KEY,
    temperature=0
)

def start_node(state: State):
    state["llm_input"] = f"Usuario dice: {state.get('user_input')}"
    return state

def reasoning_node(state: State):
    response = llm.invoke(f"Responde brevemente a: {state['llm_input']}")
    state["llm_output"] = response.content
    return state

def end_node(state: State):
    return state

graph = StateGraph(State)
graph.add_node("start", start_node)
graph.add_node("reasoning", reasoning_node)
graph.add_node("end", end_node)

graph.set_entry_point("start")
graph.add_edge("start", "reasoning")
graph.add_edge("reasoning", "end")
graph.set_finish_point("end")

agent_graph = graph.compile()
