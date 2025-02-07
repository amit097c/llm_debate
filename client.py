import requests
import json
import time
URL = 'http://localhost:8000'
#thread_id = None
trump_thread_id = ""
trudeau_thread_id = ""
turn="Trudeau"

#turn="Trudeau" trump_thread_id="" trudeau_thread_id=""
def send_prompt(message):
    #global thread_id
    global trump_thread_id
    global trudeau_thread_id
    print("Sending prompt to server: ", message)
    #data = { 'prompt': message }
    data = {
        'prompt': message,
        'turn': turn,
        'thread_id': trump_thread_id if turn == "Trump" else trudeau_thread_id
    }

    headers = {'Content-Type': 'application/json'}

    
    response = requests.post(URL, data=json.dumps(data), headers=headers)
        # Update the thread_id from the server's response
    

    if response.status_code == 200:
        response_data=response.json()
        if turn == "Trump":
            trump_thread_id = response_data.get("thread_id", trump_thread_id)
        else:
            trudeau_thread_id = response_data.get("thread_id", trudeau_thread_id)
        return response_data["message"]
        #return response_data["message"]
    
       # print("this is response: ", response_data)
    ''' if "thread_id" in response_data:
             thread_id = response_data["thread_id"]
             print("updating thread id to ",thread_id)'''
        #return response_data["message"]
    return None
message = input("client: ")
count=0
while True:
    #message = input("client: ")
    if message is None or message.lower() in ['q']:
        break
    response = send_prompt(message)
    print("Server: ", response)
    turn = "Trudeau" if turn == "Trump" else "Trump"
    print("Now its: ",turn," turn")
    # time.sleep(3) 
    count = count+1
    if count==3:
        break

'''
limit=3""
while True
   call_llm()
   call_llm()
   count++
   if(count==limit)break;
          '''