#Imports for Email Creation
import os.path
import base64
from email.message import EmailMessage

#Imports for using google API
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.errors import HttpError

#Imports to setup the backend service
from fastapi import FastAPI, HTTPException
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from .orderinformation import OrderInformation
from .cakeinformation import CakeInformation
import pandas as pd
import json

# We open up the json file and load it to your static variable
CAKES = []
with open("AllCakes.json") as AllCakeFile:
    CAKES = json.load(AllCakeFile)

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

###################################
#### Set up backend API server ####
###################################
origins = [
    "http://localhost:4200"
]
# For whatever reason add_middleware does not work
# as it should so we must do it this way when first
# Creatign the fastAPI app.
middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
]

app = FastAPI(middleware=middleware)

# API callables
@app.post("/order")
def send_mail(orderInfo: OrderInformation):
    creds = _get_credentials()
    try:
        gservice = build("gmail", "v1", credentials=creds)
        _forward_order(orderInfo, gservice)
        # Technically we should only send this if we preform
        # the previous function successfully
        _order_received(orderInfo, gservice)
        
    except HttpError as error:
        print("There was an HTTP Error: ")
        return {error}
    
    return {"It":"Worked!"}

@app.get("/cakes")
def get_cakes():
    if os.path.exists("cakeInfo.json"):
        with open("cakeInfo.json") as cakedata:
            cakeinfo = json.load(cakedata)
            return cakeinfo
    else:
        raise HTTPException(status_code="500", detail="Could not find the information on the server")
    
@app.get("/tarts")
def get_tarts():
    if os.path.exists("tartInfo.json"):
        with open("tartInfo.json") as tartdata:
            tartinfo = json.load(tartdata)
            return tartinfo
    else:
        raise HTTPException(status_code="500", detail="Could not find the information on the server")

@app.get("/others")
def get_others():
    if os.path.exists("otherInfo.json"):
        with open("otherInfo.json") as otherdata:
            otherinfo = json.load(otherdata)
            return otherinfo
    else:
        raise HTTPException(status_code="500", detail="Could not find the information on the server")
    
@app.get("/allcakes")
def get_allcakes() -> list[CakeInformation]:
    if os.path.exists("products.json"):
        with open("products.json") as alldata:
            allinfo = json.load(alldata)
            return allinfo
    else:
        raise HTTPException(status_code="500", detail="Could not find the information on the server")

    
@app.get("/cakes/{productId}")
def get_cakebyname(productId: str) -> CakeInformation:
    if CAKES == []:
        raise HTTPException(status_code="500", detail="Could not find the information on the server")
    return CAKES[productId]

##############################
#### API helper functions ####
##############################
def _get_credentials() -> Credentials:
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", scopes=SCOPES)
      # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds

def _order_received(orderinfo: OrderInformation, gservice: any):
    message = EmailMessage()

    message.set_content(
        "This email is to say that we have received your order and we will be in contact with you shortly!\n\n" +
        "This is an automated message, please do not reply as this inbox is not monitored."
    )
    message["To"] = "Jarrick_pang@hotmail.com"
    message["From"] = "haoautreply@gmail.com"
    message["Subject"] = "Your Cake Order Has been Received!"

    _send_message(gservice, message)


def _forward_order(orderinfo: OrderInformation, gservice: any):
    message = EmailMessage()

    message.set_content(
        f"We've received a new order from {orderinfo.name}!!!!!\n"
        "cake:" + orderinfo.cakeName + "\n" +
        "size:" + orderinfo.cakeSize + "\n" +
        "pickup:" + orderinfo.pickupdate + "\n" +
        "allergies:" + orderinfo.allergies + "\n" + 
        "lactose free:" + str(orderinfo.lactose) + "\n" +
        "message:" + orderinfo.message + "\n" +
        "email:" + orderinfo.email
    )
    message["To"] = "Jarrick_pang@hotmail.com"
    message["From"] = "haoautreply@gmail.com"
    message["Subject"] = "New Order Receieved!"

    _send_message(gservice, message)

# Given a message we send it through with the google service
def _send_message(gservice: any, message: EmailMessage):
        # Encode message, gmail api uses base64url encoded strings
        # https://developers.google.com/gmail/api/guides/sending
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        create_message = {"raw": encoded_message}

        send_message = (
            gservice.users()
            .messages()
            .send(userId="me", body=create_message)
            .execute()
        )
