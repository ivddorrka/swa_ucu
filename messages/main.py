import hazelcast
from fastapi import FastAPI, Request
import time

client = hazelcast.HazelcastClient(

    cluster_members=["172.17.0.5:5701", "172.17.0.6:5701"]

)


queue = client.get_queue("distributed-queue").blocking()



app = FastAPI()

@app.post('/')
async def create2_message(request: Request):
    data = await request.json()
    message = data.get("message")
    
    global queue
    queue.put(message)
    return {"message": f"{message}: added to the queue"}


@app.get('/')
async def read_messages():
    global queue
    messages = []
    while queue.size() != 0: 
        message = queue.take()
        messages.append(message)
    for mes in messages:
        queue.put(mes)
        time.sleep(0.5)
    return {"messages": messages}

if __name__ =="__main__":
    import uvicorn
    import sys

    port = int(sys.argv[1])
    uvicorn.run(app, host='localhost', port=port)
