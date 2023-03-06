import httpx
from fastapi import FastAPI

app = FastAPI()

message_endpoint = "http://localhost:8082/"


@app.get('/')
async def get_message_response():
    return "[Not implemented yet]: "

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8082, log_level="debug")