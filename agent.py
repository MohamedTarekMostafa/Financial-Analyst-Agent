from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
from langchain_google_genai import ChatGoogleGenerativeAI
from tools import financial_tools 
from dotenv import load_dotenv

load_dotenv()

class State(TypedDict):
    messages: Annotated[list, add_messages]

def create_agent():
    llm = ChatGoogleGenerativeAI(model='gemini-2.5-flash', temperature=0)
    llm_with_tools = llm.bind_tools(financial_tools)

    def llm_node(state: State):
        return {"messages": [llm_with_tools.invoke(state["messages"])]}

    builder = StateGraph(State)
    
    builder.add_node("llm", llm_node)
    
    tool_node = ToolNode(financial_tools)
    builder.add_node("tools", tool_node)

    builder.add_edge(START, "llm")
    
    builder.add_conditional_edges("llm", tools_condition)
    
    builder.add_edge("tools", "llm")

    return builder.compile(checkpointer=MemorySaver())