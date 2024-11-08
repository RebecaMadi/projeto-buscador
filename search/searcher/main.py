from fastapi import FastAPI, HTTPException
from typing import Dict, Any
from searcher.controllers.controller import search_controller, search_postgres_controller
import logging

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/search")
async def search(request: Dict[str, Any]):

    if not request.get("query"):
            raise HTTPException(status_code=400, detail="Query is required.")
    return search_controller(request)

@app.post("/searchbyid")
async def search(request: Dict[str, Any]):

    if not request.get("id"):
            raise HTTPException(status_code=400, detail="Id is required.")
    return search_postgres_controller(request.get("id"))