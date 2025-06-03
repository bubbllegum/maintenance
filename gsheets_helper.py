from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from googleapiclient.errors import HttpError

# Ganti dengan path file credential JSON kamu
SERVICE_ACCOUNT_FILE = 'credentials.json'

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

credentials = Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

service = build('sheets', 'v4', credentials=credentials)

class Worksheet:
    def __init__(self, service, spreadsheet_id, worksheet_name):
        self.service = service
        self.spreadsheet_id = spreadsheet_id
        self.worksheet_name = worksheet_name

    def append_row(self, values):
        body = {
            "values": [values]
        }
        range_ = f"{self.worksheet_name}!A1"
        result = self.service.spreadsheets().values().append(
            spreadsheetId=self.spreadsheet_id,
            range=range_,
            valueInputOption="USER_ENTERED",
            insertDataOption="INSERT_ROWS",
            body=body
        ).execute()
        return result

def worksheet_exists(spreadsheet_id: str, worksheet_name: str) -> bool:
    spreadsheet = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
    sheet_titles = [sheet['properties']['title'] for sheet in spreadsheet['sheets']]
    return worksheet_name in sheet_titles

def open_sheet(spreadsheet_id: str, worksheet_name: str):
    """Membuka worksheet/tab bernama worksheet_name di spreadsheet."""
    if not worksheet_exists(spreadsheet_id, worksheet_name):
        raise ValueError(f"Worksheet '{worksheet_name}' tidak ditemukan.")
    return Worksheet(service, spreadsheet_id, worksheet_name)

def create_worksheet(spreadsheet_id: str, worksheet_name: str, rows: int = 1000, cols: int = 5):
    """Membuat worksheet/tab baru dengan nama worksheet_name."""
    requests = [{
        "addSheet": {
            "properties": {
                "title": worksheet_name,
                "gridProperties": {
                    "rowCount": rows,
                    "columnCount": cols
                }
            }
        }
    }]
    body = {'requests': requests}
    try:
        response = service.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body=body
        ).execute()
        return response
    except HttpError as e:
        print(f"Error saat membuat worksheet: {e}")
        raise

def create_worksheet_with_header(spreadsheet_id: str, worksheet_name: str, headers: list):
    """
    Membuat worksheet/tab baru dan langsung menulis header kolom.
    """
    create_worksheet(spreadsheet_id, worksheet_name, rows=1000, cols=len(headers))

    body = {
        "values": [headers]
    }
    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=f"{worksheet_name}!A1",
        valueInputOption="USER_ENTERED",
        body=body
    ).execute()
