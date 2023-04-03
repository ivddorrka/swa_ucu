import httpx
import random 
from fastapi import FastAPI, Header, Response, Request

app = FastAPI()

uuid = 1

facade_endpoint = "http://localhost:8080/"
logging_endpoint = ["http://localhost:8081/","http://localhost:8083", "http://localhost:8084"]
message_endpoint = "http://localhost:8082/"


@app.get("/")
async def get_messages():
    async with httpx.AsyncClient() as client:
        try:
            log_response1 = await client.get(logging_endpoint[0])
        except httpx.ConnectError:
            pass

        try:
            log_response2 = await client.get(logging_endpoint[1])
        except httpx.ConnectError:
            pass        
        try:
            log_response3 = await client.get(logging_endpoint[2])
        except httpx.ConnectError:
            pass        
        mess_response = await client.get(message_endpoint)


    log_rsp = ""
    try:
        log_response1.raise_for_status()
        log_rsp += str(log_response1.json()) + " "
    except:
        pass
    try:
        log_response2.raise_for_status()
        log_rsp += str(log_response2.json()) + " "
    except:
        pass
    try:
        log_response3.raise_for_status()
        log_rsp += str(log_response3.json()) + " "
    except:
        pass

    mess_response.raise_for_status()

    output_response = str(mess_response.json()) + log_rsp
    return output_response

import requests
def random_choice_of_logging_endpoint():

    found_endpoint = False
    endpoint = ""

    while not found_endpoint:
        endpoint = random.choice(logging_endpoint)
        try:
            response = requests.get(endpoint)
            if response.status_code == 200:
                found_endpoint = True
        except requests.exceptions.RequestException as e:
            pass
    return endpoint



@app.post("/", status_code=201)
async def create_message(request: Request):
    global uuid

    data = await request.json()
    message = data.get("message")
    lg_endpoint = random_choice_of_logging_endpoint()
    if message:
        async with httpx.AsyncClient() as client:
            response = await client.post(lg_endpoint, json={'message': message, 'uuid': uuid})

    response.raise_for_status()
    uuid += 1
    return {"message": f"Received message: {message}"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8080, log_level="debug")