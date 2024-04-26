from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .libs.CouchDBClient import CouchDBClient
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

PATIENTS_DB = "patients"

class Relative(BaseModel):
    first_name: str
    last_name: str
    relation: str
    email: str
    phone_number: str

class Patient(BaseModel):
    first_name: str
    last_name: str
    picture: str
    age: int
    sex: str
    diagnosis: str
    prognosis: str
    wish: str
    relatives: list[Relative] = []

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
        couchdb_client.createDatabase(PATIENTS_DB)
    except Exception:
        pass

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/patients/")
async def create_patient() -> list[Patient]:
    patient_keys = couchdb_client.listDocuments(PATIENTS_DB)
    patients = []
    for key in patient_keys:
        patient = couchdb_client.getDocument(PATIENTS_DB, key)
        patients.append(patient)
    return {"patients": patients}

@app.post("/patients/")
async def create_patient(patient: Patient) -> Patient:
    patient_as_json = jsonable_encoder(patient)
    key = couchdb_client.addDocument(PATIENTS_DB, patient_as_json) 
    new_patient = couchdb_client.getDocument(PATIENTS_DB, key)
    return {"patient": new_patient}
