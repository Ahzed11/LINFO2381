from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP, SMTPException
import smtplib
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .libs.CouchDBClient import CouchDBClient
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from typing import Optional
import os

#region CONSTANTS
PATIENTS_DB = "patients"
#endregion

#region CLASSES
class Relative(BaseModel):
    first_name: str
    last_name: str
    relation: str
    email: Optional[str] = None
    phone_number: Optional[str] = None

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
    except Exception:
        pass
#endregion

#region API ENDPOINTS
@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/patients/")
async def list_patients():
    patient_keys = couchdb_client.listDocuments(PATIENTS_DB)
    patients = []
    for key in patient_keys:
        patient = couchdb_client.getDocument(PATIENTS_DB, key)
        patients.append(patient)
    return patients

@app.get("/patients/{patient_id}")
def get_patient(patient_id: str):
    patient = couchdb_client.getDocument(PATIENTS_DB, patient_id)

    return patient

@app.post("/patients/")
async def create_patient(patient: Patient):
    patient_as_json = jsonable_encoder(patient)
    key = couchdb_client.addDocument(PATIENTS_DB, patient_as_json) 
    new_patient = couchdb_client.getDocument(PATIENTS_DB, key)
    return  new_patient


@app.post("/patients/{patient_id}/notify-relatives")
async def submit_wish(patient_id: str):
    patient = couchdb_client.getDocument(PATIENTS_DB, patient_id)

    for relative in patient["relatives"]:
        email = relative["email"]
        wish = patient["wish"]
        result = send_email(email, wish)
        if result:
            return {"message": "Wish submitted and email sent successfully."}
        else:
            raise HTTPException(status_code=500, detail="Email could not be sent.")


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
