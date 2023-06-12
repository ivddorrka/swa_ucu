import httpx
import random 
from fastapi import FastAPI, Header, Response, Request

app = FastAPI()

uuid = 1

facade_endpoint = "http://localhost:8080/"
logging_endpoint = ["http://localhost:8081/","http://localhost:8083", "http://localhost:8084"]
message_endpoint = ["http://localhost:8082/", "http://localhost:8085/"]


@app.get("/")
async def get_messages():
    async with httpx.AsyncClient() as client:
        timeout = httpx.Timeout(10.0, read=None)
        try:
            log_response1 = await client.get(logging_endpoint[0], timeout=timeout)
        except httpx.ConnectError:
            pass

        try:
            log_response2 = await client.get(logging_endpoint[1], timeout=timeout)
        except httpx.ConnectError:
            pass        
        try:
            log_response3 = await client.get(logging_endpoint[2], timeout=timeout)
        except httpx.ConnectError:
            pass    
        try:    
            mess_response1 = await client.get(message_endpoint[0], timeout=timeout)
        except httpx.ConnectError:
            pass    
        try:
            mess_response2 = await client.get(message_endpoint[1], timeout=timeout)
        except httpx.ConnectError:
            pass    


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
    
    mess_responces = []
    try:
        mess_response1.raise_for_status()
        mess_responces.append(mess_response1)
    except:
        pass

    try:
        mess_response2.raise_for_status()
        mess_responces.append(mess_response2)
    except:
        pass

    mess_response_final = random.choice(mess_responces)


    output_response = f"Message endpoint random responce: {str(mess_response_final.json())}; Log Responce: {log_rsp}"
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

def available_message_endpoint():

    endpoints_list = []

    for i in message_endpoint:
        endpoint = i
        try:
            response = requests.get(endpoint)
            if response.status_code == 200:
                endpoints_list.append(endpoint)
        except requests.exceptions.RequestException as e:
            pass
    return endpoints_list


@app.post("/", status_code=201)
async def create_message(request: Request):
    global uuid

    data = await request.json()
    message = data.get("message")
    lg_endpoint = random_choice_of_logging_endpoint()
    mssgs_edpoints = available_message_endpoint()
    if message:
        async with httpx.AsyncClient() as client:
            response = await client.post(lg_endpoint, json={'message': message, 'uuid': uuid})
            for endp in mssgs_edpoints:
                response = await client.post(endp, json={'message': message})
            # response = await client.post(message_endpoint[1], json={'message': message})

    response.raise_for_status()
    uuid += 1
    return {"message": f"Received message: {message}"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8080, log_level="debug")
