from llm import trudeau_llm,trudeau_tools
from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph import START,END
from langgraph.graph.message import add_messages,StateGraph
from langchain_core.prompts import MessagesPlaceholder,ChatPromptTemplate
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode,tools_condition
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

class DebateState(TypedDict):
    messages:Annotated[list,add_messages] # messages is list of messages to perseve the context of conversation
    language:str

  
MAX_TURNS=3
workflow2=StateGraph(DebateState)

def conclude(state:DebateState):
    '''Conclude the conversation with a diplomatic statement in Trudeau's style.'''
    try:
        prompt_template=ChatPromptTemplate([("system","assert  concluding statements in trudea's diplomatic assertive style"),MessagesPlaceholder("messages")])
        prompt = prompt_template.invoke(state)
        response = trudeau_llm.invoke(prompt)
        state["messages"].append(response)
        return {"messages": response}
    except Exception as e:
        logging.error(f"Error in conclude function: {e}")
        state["messages"].append({"role": "system", "content": "Sorry, an error occurred while concluding the conversation."})
        return {"messages": "Error occurred"} 

def should_conclude(state: DebateState)->bool:
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

def invoke_trudeau_llm(state:DebateState):
    
    logging.info(f"(Trudeau) invoke_llm method()")
    try:
        # if state.get("turn_count") >= MAX_TURNS:
        #     return conclude(state)
        prompt_template=ChatPromptTemplate([("system", "You must keep your tone polished, empathetic, and inclusive, mirroring Justin Trudeau's diplomatic style responding to Trump.Be brief, clear, and to the point. Use short, impactful statements, avoiding unnecessary elaboration. Summarize arguments effectively in 2-3 sentences per response."),MessagesPlaceholder("messages")])

        prompt=prompt_template.invoke(state)
        response=trudeau_llm.invoke(prompt)

        logging.info(f"Response: {response}")
        return {"messages":response}
    except Exception as e:
        logging.error(f"Error in invoke_trudeau_llm: {e}")
        state["messages"].append({"role": "system", "content": "Sorry, an error occurred. Please try again later."})
        return {"messages": "Error occurred"}


workflow2.add_edge(START,"trudeau_home")
workflow2.add_node("trudeau_home",invoke_trudeau_llm) #trudeau llm

#added a new node conclude
workflow2.add_node("conclude",conclude)

trudeau_tool_node=ToolNode(trudeau_tools)
workflow2.add_node("tools",trudeau_tool_node)
workflow2.add_conditional_edges("trudeau_home",tools_condition,["tools",END])

#added a conditional edge to conclude node based on a condition then it should end and return the response
#workflow2.add_conditional_edges("trudeau_home", should_conclude, ["conclude", END])

#added a conditional edge to conclude node based on a condition then it should end and return the response
# workflow2.add_conditional_edges("trudeau_home", lambda: TURN_COUNT >= MAX_TURNS, ["conclude", END])




#graph.add_conditional_edges(START, routing_function, {True: "node_b", False: "node_c"})
workflow2.add_conditional_edges(
    "trudeau_home",
    should_conclude,
    {True: "conclude", False: END}
)
workflow2.add_edge("tools",END)
workflow2.add_edge("conclude", END)

memory = MemorySaver() # MemorySaver() creates a tool called MemorySaver. Think of this tool as a notebook where important information about the conversation is written down so it can be remembered later.
trudeau_graph=workflow2.compile(checkpointer=memory) # tells the program to use this notebook (the MemorySaver) as a checkpointer when organizing and managing the workflow. The checkpointer parameter is essentially a way to tell the workflow to use the MemorySaver to keep track of its state.
