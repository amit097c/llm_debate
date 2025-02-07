from llm import trudeau_llm,trudeau_tools
from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph import START,END
from langgraph.graph.message import add_messages,StateGraph
from langchain_core.prompts import MessagesPlaceholder,ChatPromptTemplate
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode,tools_condition

class DebateState(TypedDict):
    messages:Annotated[list,add_messages] # messages is list of messages to perseve the context of conversation
    language:str


workflow2=StateGraph(DebateState)

def invoke_trudeau_llm(state:DebateState):
    prompt_template=ChatPromptTemplate([("system", "You must keep your tone polished, empathetic, and inclusive, mirroring Justin Trudeau's diplomatic style responding to Trump.Be brief, clear, and to the point. Use short, impactful statements, avoiding unnecessary elaboration.ummarize arguments effectively in 2-3 sentences per response."),MessagesPlaceholder("messages")])
    # ("user", last_message)
    prompt=prompt_template.invoke(state)
    response=trudeau_llm.invoke(prompt)
    return {"messages":response}

workflow2.add_edge(START,"trudeau_home")
workflow2.add_node("trudeau_home",invoke_trudeau_llm) #trudeau llm

trudeau_tool_node=ToolNode(trudeau_tools)
workflow2.add_node("tools",trudeau_tool_node)
workflow2.add_conditional_edges("trudeau_home",tools_condition,["tools",END])

#workflow.add_edge("tools","home")
workflow2.add_edge("tools","trudeau_home")
memory = MemorySaver() # MemorySaver() creates a tool called MemorySaver. Think of this tool as a notebook where important information about the conversation is written down so it can be remembered later.
trudeau_graph=workflow2.compile(checkpointer=memory) # tells the program to use this notebook (the MemorySaver) as a checkpointer when organizing and managing the workflow. The checkpointer parameter is essentially a way to tell the workflow to use the MemorySaver to keep track of its state.
