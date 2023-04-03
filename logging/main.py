from fastapi import FastAPI, Request
from hazelcast import HazelcastClient
import sys
import uvicorn

hazelcast_client = HazelcastClient(
    cluster_members=["172.17.0.2:5701", "172.17.0.3:5701", "172.17.0.4:5701"],
    cluster_name="dev"
)

hz_map = hazelcast_client.get_map("hz_map").blocking()
app = FastAPI()

@app.get('/')
async def get_response():
    map_values = hz_map.values()    
    return "\n".join(map_values)

@app.post('/')
async def create2_message(request: Request):
    data = await request.json()
    message = data.get("message")
    uuid = data.get('uuid')

    print(f"UUID={uuid} of message '{message}'")
    hz_map.put(uuid, message)
    return {"message": f"Received message {uuid}: {message}"}


if __name__ == "__main__":
    
    port = int(sys.argv[1])
    uvicorn.run(app, host="localhost", port=port)