from llm import llm,tools,trudeau_llm,trudeau_tools
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


workflow=StateGraph(DebateState)
def invoke_llm(state:DebateState):
    # prompt_template=ChatPromptTemplate([("system","You must keep your tone conversational, spartan"),
    #                                     MessagesPlaceholder("messages")])  #MessagesPlaceholder class handles the dynamic insertion of user and system messages into the chat prompt, ensuring that the conversation context is maintained.
    
    prompt_template=ChatPromptTemplate([("system", "You must keep your tone conversational, spartan, and bold, mirroring Donald Trump's unique style to respond to Justin Trudeau. Be confident, assertive, and unapologetic this is debate with trudeau. Use simple, direct language, repetition, and hyperbole to emphasize your points. Deflect questions you can't answer by pivoting to related topics or attacking the source. Always tie your responses back to your own achievements or abilities, framing yourself as the ultimate problem-solver. Use anecdotes and emotional appeals to connect with the audience, and end on an optimistic note, promising to 'fix' the issue better than anyone else."),
                                         MessagesPlaceholder("messages")])
    prompt=prompt_template.invoke(state)
    response=llm.invoke(prompt)
    return {"messages":response}

workflow.add_edge(START,"home")
workflow.add_node("home",invoke_llm) # trump llm

tool_node=ToolNode(tools)
workflow.add_node("tools",tool_node)
    
workflow.add_conditional_edges("home",tools_condition,["tools",END])


#workflow.add_edge("tools","home")
workflow.add_edge("tools","home")

memory = MemorySaver() # MemorySaver() creates a tool called MemorySaver. Think of this tool as a notebook where important information about the conversation is written down so it can be remembered later.
graph=workflow.compile(checkpointer=memory) # tells the program to use this notebook (the MemorySaver) as a checkpointer when organizing and managing the workflow. The checkpointer parameter is essentially a way to tell the workflow to use the MemorySaver to keep track of its state.

