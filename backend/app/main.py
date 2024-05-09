from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .libs.CouchDBClient import CouchDBClient
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field
import os
import json

#region CONSTANTS
PATIENTS_DB = "patients"
#endregion

#region CLASSES
class Relative(BaseModel):
    first_name: str
    last_name: str
    relation: str
    email: str | None = None
    phone_number: str | None = None

class Patient(BaseModel):
    first_name: str
    last_name: str
    picture: str | None = None
    birthdate: str
    sex: str
    diagnosis: str
    prognosis: str
    wish: str
    relatives: list[Relative] = []

class PatientFromDB(Patient):
    id: str | None = Field(alias="_id", default=None)
    rev: str | None = Field(alias="_rev", default=None)

class Message(BaseModel):
    message: str

#endregion

#region FASTAPI/COUCHDB SETUP
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

couchdb_client = CouchDBClient(url="http://couchdb:5984")
#endregion

#region FASTAPI EVENTS
@app.on_event("startup")
async def startup_event():
    try:
        couchdb_client.createDatabase(PATIENTS_DB)

        # TODO: Insert patients from PatientModels
        # Load all three patiens from the PatientModels
        # Insert them into the database
        
        # JSON Path to the file
        path = os.path.join(os.path.dirname(__file__), "PatientModels")
        
        # List dir
        files = os.listdir(path)
        
        # Iterate over the files
        for file in files:
            with open(os.path.join(path, file), "r") as f:
                patient_as_json = json.load(f)
                key = couchdb_client.addDocument(PATIENTS_DB, patient_as_json)
                print("Added patient to couchdb with key: ", key)
    except Exception:
        pass
#endregion

#region API ENDPOINTS

@app.get("/patients/")
async def list_patients() -> list[PatientFromDB]:
    patient_keys = couchdb_client.listDocuments(PATIENTS_DB)
    patients = []
    for key in patient_keys:
        patient = couchdb_client.getDocument(PATIENTS_DB, key)
        patients.append(patient)
    return patients

@app.get("/patients/{patient_id}")
def get_patient(patient_id: str) -> PatientFromDB:
    try:
        patient = couchdb_client.getDocument(PATIENTS_DB, patient_id)
        return patient
    except Exception:
        raise HTTPException(status_code=404, detail="Patient does not exist")

@app.post("/patients/")
async def create_patient(patient: Patient) -> PatientFromDB:
    patient_as_json = jsonable_encoder(patient)
    key = couchdb_client.addDocument(PATIENTS_DB, patient_as_json) 
    new_patient = couchdb_client.getDocument(PATIENTS_DB, key)
    return  new_patient


@app.post("/patients/{patient_id}/notify-relatives")
async def notify_relatives(patient_id: str) -> Message:
    patient: PatientFromDB | None = None
    
    try:
        patient_document = couchdb_client.getDocument(PATIENTS_DB, patient_id)
        patient = PatientFromDB.parse_obj(patient_document)
    except Exception:
        raise HTTPException(status_code=404, detail="Patient does not exist")

    wish = patient.wish
    for relative in patient.relatives:
        email = relative.email
        
        result = send_email(email, wish)
        if not result:
            raise HTTPException(status_code=500, detail="Email could not be sent.")
        
    return {"message": "Wish submitted and email sent successfully."}

#endregion

#region utils

def send_email(recipient_email: str, death_wish: str):
    sender_email = "test"

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = recipient_email
    message['Subject'] = 'Notification of Death Wish Submission'

    message_body = f"Hello,\n This is the wish of your relative: {death_wish} \n Have a nice day !"
    message.attach(MIMEText(message_body, 'plain'))

    try:
        with smtplib.SMTP(host="mailbox", port=1025) as smtp:
            smtp.send_message(message)
            return True
    except smtplib.SMTPException as e:
        print(f"Failed to send email: {e}")
        return False

#endregion