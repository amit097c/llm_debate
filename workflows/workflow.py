from llm import llm,tools,trudeau_llm,trudeau_tools
from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph import START,END
from langgraph.graph.message import add_messages,StateGraph
from langchain_core.prompts import MessagesPlaceholder,ChatPromptTemplate
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode,tools_condition
import logging

logging.basicConfig(level=logging.INFO)

class DebateState(TypedDict):
    messages:Annotated[list,add_messages] # messages is list of messages to perseve the context of conversation
    language:str
    turn_count:int


MAX_TURNS=3
workflow=StateGraph(DebateState)

def should_conclude(state: DebateState):
    messages = state.get("messages", [])
    if not messages:
        return False
    last_message = messages[-2]  # Get the last message in the list
    logging.info("last_message format: ",last_message)
    last_message_text=""
    if hasattr(last_message, "content"):
        last_message_text = last_message.content
    contains_conclude = "---conclude debate---" in last_message_text
    logging.info(f"state['messages'] contains substring '---conclude debate---' at the end: {contains_conclude}")
    return contains_conclude

def conclude(state:DebateState):
    '''Conclude with sarcastic bold assertive trump style statement'''
    try:         
        prompt_template=ChatPromptTemplate([("system","conclude in bold assertive trump style, keep the tone bold, spartan and make a sarcastic funny conclusion"),MessagesPlaceholder("messages")])
        prompt = prompt_template.invoke(state)
        response = trudeau_llm.invoke(prompt)
        state["messages"].append(response)
        logging.info(f"concluding statement with turn_count:{state.get("turn_count")}")
        return {"messages": response}
    except Exception as e:
         logging.error(f"Error in conclude function: {e}")
         state["messages"].append({"role": "system", "content": "Sorry, an error occurred while concluding the conversation."})
         return {"messages": "Error occurred"} 


def invoke_llm(state:DebateState):
    # logging.info(f"invoke_llm method()-> updating turn_count value to: {state["turn_count"]} ")
    try:         
        # if state["turn_count"]>= MAX_TURNS:
        #     return conclude(state)
        # logging.info(f"(Trump)invoke_llm method()-> updating turn_count value to: {state["turn_count"]} ")
        prompt_template=ChatPromptTemplate([("system", "You must keep your tone conversational, spartan, and bold, mirroring Donald Trump's unique style to respond to Justin Trudeau. Be confident, assertive, and unapologetic this is debate with trudeau. Use simple, direct language, repetition, and hyperbole to emphasize your points. Deflect questions you can't answer by pivoting to related topics or attacking the source. Always tie your responses back to your own achievements or abilities, framing yourself as the ultimate problem-solver. Use anecdotes and emotional appeals to connect with the audience, and end on an optimistic note, promising to 'fix' the issue better than anyone else."),
                                            MessagesPlaceholder("messages")])
        prompt=prompt_template.invoke(state)
        response=llm.invoke(prompt)
        return {"messages":response}
    except Exception as e:
        logging.error(f"Error in (Trump) invoke_llm: {e}")
        state["messages"].append({"role":"system","content":"Sorry, an error occurred. Please try again later."}) 
        return {"messages": "Error occurred"}
workflow.add_edge(START,"home")
workflow.add_node("home",invoke_llm) # trump llm

tool_node=ToolNode(tools)
workflow.add_node("tools",tool_node)
    
workflow.add_conditional_edges("home",tools_condition,["tools",END])
workflow.add_conditional_edges(
    "home",
    should_conclude,
    {True: "conclude", False: END}
)
#added a new node conclude
workflow.add_node("conclude",conclude)
workflow.add_edge("tools",END)
workflow.add_edge("conclude", END)



#workflow.add_edge("tools","home")
workflow.add_edge("tools","home")

memory = MemorySaver() # MemorySaver() creates a tool called MemorySaver. Think of this tool as a notebook where important information about the conversation is written down so it can be remembered later.
graph=workflow.compile(checkpointer=memory) # tells the program to use this notebook (the MemorySaver) as a checkpointer when organizing and managing the workflow. The checkpointer parameter is essentially a way to tell the workflow to use the MemorySaver to keep track of its state.

