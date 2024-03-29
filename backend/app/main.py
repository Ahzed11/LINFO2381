from fastapi import FastAPI
from .libs.CouchDBClient import CouchDBClient

app = FastAPI()
couchdb_client = CouchDBClient(url="http://couchdb:5984")

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
