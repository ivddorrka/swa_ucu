import httpx

from fastapi import FastAPI, Header, Response, Request

app = FastAPI()

uuid = 1

facade_endpoint = "http://localhost:8080/"
logging_endpoint = "http://localhost:8081/"
message_endpoint = "http://localhost:8082/"


@app.get("/")
async def get_messages():
    async with httpx.AsyncClient() as client:
        log_response = await client.get(logging_endpoint)
        mess_response = await client.get(message_endpoint)

    log_response.raise_for_status()
    mess_response.raise_for_status()

    output_response = str(mess_response.json()) + str(log_response.json()) 
    return output_response


@app.post("/", status_code=201)
async def create_message(request: Request):
    global uuid

    data = await request.json()
    message = data.get("message")
    if message:
        async with httpx.AsyncClient() as client:
            response = await client.post(logging_endpoint, json={'message': message, 'uuid': uuid})

    response.raise_for_status()
    uuid += 1
    return {"message": f"Received message: {message}"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8080, log_level="debug")