from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import pickle
import os
from config import SPREADSHEET_ID, SHEET_NAME

TOKEN_FILE = "credentials/token.pickle"


def get_sheets_service():
    with open(TOKEN_FILE, "rb") as f:
        creds = pickle.load(f)

    return build("sheets", "v4", credentials=creds)


def append_row(service, row):
    service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=f"{SHEET_NAME}!A:D",
        valueInputOption="RAW",
        body={"values": [row]}
    ).execute()
