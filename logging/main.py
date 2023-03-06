from fastapi import FastAPI, Request

app = FastAPI()
messages_allocs = {}

logging_endpoint = "http://localhost:8081/"



@app.get('/')
async def get_response():
    return str(messages_allocs)

@app.post('/')
async def create2_message(request: Request):
    data = await request.json()
    message = data.get("message")
    uuid = data.get('uuid')

    global messages_allocs
    print(f"UUID={uuid} of message '{message}'")
    messages_allocs[uuid]=message
    return {"message": f"Received message XXXXXX: {message}"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8081, log_level="debug")
