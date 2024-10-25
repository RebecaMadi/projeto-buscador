from fastapi import FastAPI, Query
from typing import Optional
from coletasapi.controllers import search_processo_controller
from coletasapi.connections.lawsuit_raw_producer import produce
import json

app = FastAPI()


@app.get("/")
def read_root():
    return {"coletasapi": "Hello World!"}


@app.get("/lawsuit")
async def get_lawsuit(lawsuit_number: str, max_cache_age_seconds: int):
    print(max_cache_age_seconds)
    response = search_processo_controller(lawsuit_number, max_cache_age_seconds)
    utf8_responses = []

    if not isinstance(response, list):
        response = [response]

    for resp in response:
        if "error" not in resp.keys():
            await produce(resp)

        utf8_resp = json.dumps(resp, ensure_ascii=False).encode('utf-8')
        utf8_responses.append(json.loads(utf8_resp))

    return utf8_responses