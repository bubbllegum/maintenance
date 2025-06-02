import streamlit as st
from gsheets_helper import open_sheet
import pandas as pd
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

SPREADSHEET_ID = "1sELnjwsgObSAtfAf2tGZSGvj47dfYC1ESDZSaXqTN4g"
SERVICE_ACCOUNT_FILE = 'credentials.json'

def get_worksheet_names(spreadsheet_id):
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

    credentials = Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    service = build('sheets', 'v4', credentials=credentials)
    spreadsheet = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()

    sheet_titles = [sheet['properties']['title'] for sheet in spreadsheet['sheets']]
    return sheet_titles

def get_worksheet_data(worksheet):
    result = worksheet.service.spreadsheets().values().get(
        spreadsheetId=worksheet.spreadsheet_id,
        range=f"{worksheet.worksheet_name}!A1:Z1000"
    ).execute()

    values = result.get('values', [])
    if not values:
        return pd.DataFrame()

    header = values[0]
    data_rows = values[1:]

    # Sesuaikan panjang data setiap baris dengan header
    for i in range(len(data_rows)):
        if len(data_rows[i]) < len(header):
            data_rows[i] += [''] * (len(header) - len(data_rows[i]))
        elif len(data_rows[i]) > len(header):
            data_rows[i] = data_rows[i][:len(header)]

    df = pd.DataFrame(data_rows, columns=header)
    return df

def show():
    st.markdown(
    "<h1 style='text-align: center; color: white;'>Maintenance terakhir</h1>", 
    unsafe_allow_html=True
)

    worksheet_names = get_worksheet_names(SPREADSHEET_ID)
    selected_sheet = st.selectbox("Pilih Worksheet (Ruangan - Alat)", worksheet_names)

    if selected_sheet:
        worksheet = open_sheet(SPREADSHEET_ID, selected_sheet)
        df = get_worksheet_data(worksheet)

        if df.empty:
            st.info("Data maintenance kosong.")
            return

        # Pastikan kolom tanggal sudah datetime
        df['Tanggal'] = pd.to_datetime(df['Tanggal'])

        # Ambil data maintenance terakhir per ruangan dan alat
        df_last = df.sort_values('Tanggal').groupby(['Ruangan', 'Nama Alat'], as_index=False).last()

        st.dataframe(df_last)
