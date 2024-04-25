from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .libs.CouchDBClient import CouchDBClient
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field

class Patient(BaseModel):
    first_name: str
    last_name: str

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

couchdb_client = CouchDBClient(url="http://couchdb:5984")

@app.on_event("startup")
async def startup_event():
    try:
        couchdb_client.createDatabase("patients")
    except Exception:
        pass

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/patients/")
async def create_patient(patient: Patient):
    patient_as_json = jsonable_encoder(patient)
    key = couchdb_client.addDocument("patients", patient_as_json) 
    new_patient = couchdb_client.getDocument("patients", key)
    return {"message": f"Hello {new_patient}"}
