from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # Import CORSMiddleware
from pydantic import BaseModel
from workflows.workflow import graph
from workflows.trudeau_workflow import trudeau_graph
from langchain_core.messages import HumanMessage
import uuid

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # Allow requests from this origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

class PromptReq(BaseModel):
    prompt: str
    thread_id: str  # Ensure thread_id is included in the model
    turn:str

thread_store = {}  # to store thread_ids

@app.get("/")
async def get():
    return {"message": "hello jello this is a debate battleground"}

@app.post("/")
async def debate(topic: PromptReq):
    print("this is server post method topic is ", topic.prompt," topic ",topic.turn," thread_id",topic.thread_id)
    unique_thread_id = topic.thread_id
    print("client thread_id: ", unique_thread_id)
    if not unique_thread_id:
        unique_thread_id = str(uuid.uuid4())
        thread_store[unique_thread_id] = {"context": []}

    config = {"configurable": {"thread_id": unique_thread_id}}  # Correct usage of unique_thread_id
    messages = {"messages": [HumanMessage(topic.prompt)]} # for a particular thread_id the context is getting retained through MemorySaver()

    if topic.turn=="Trump":
        trumps_response = graph.invoke(messages, config) 
        print("Trump: ",trumps_response["messages"][-1].content)
        return{
            "thread_id":unique_thread_id,
            "message": trumps_response["messages"][-1].content,
            "turn":topic.turn}
    else:
        trudeau_response=trudeau_graph.invoke(messages,config)
        print("Trudeau: ",trudeau_response["messages"][-1].content)
        return{
            "thread_id":unique_thread_id,
            "message": trudeau_response["messages"][-1].content,
            "turn":topic.turn}
    # messages = {"messages": [trudeaus_response["messages"][-1].content]}
    # trumps_response = graph.invoke(messages, config)
    # print("Trump: ",trumps_response["messages"][-1].content)
    # messages = {"messages": [trumps_response["messages"][-1].content]}
    # trudeaus_response=trudeau_graph.invoke(messages,config)
    # print("Trudeau: ",trudeaus_response["messages"][-1].content)
    # print(output) to check the log between user and AI with detailed metadata

    '''    for _ in range(3):  # Loop that breaks after 3 runs
        trumps_response = graph.invoke(messages, config)
        print("Trump: ", trumps_response["messages"][-1].content)
        messages = {"messages": [HumanMessage(trumps_response["messages"][-1].content)]} 
        trudeaus_response = trudeau_graph.invoke(messages, config)
        print("Trudeau: ", trudeaus_response["messages"][-1].content)
        messages = {"messages": [HumanMessage(trudeaus_response["messages"][-1].content)]}
'''
    return {
        "thread_id":unique_thread_id,
        "message": "Trump: "+trumps_response["messages"][-1].content +"  Trudeau: "+trudeaus_response["messages"][-1].content
        }