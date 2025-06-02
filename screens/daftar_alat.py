import streamlit as st
import pandas as pd
from gsheets_helper import open_sheet, create_worksheet_with_header
from datetime import datetime

SPREADSHEET_ID = "1pONEpw-ww19dOJ88vibUTuBy6PvMOBTso7Yp2LVbjAU"
HEADERS = ["NAMA ALAT", "NO SN", "MERK", "TIPE", "RUANGAN", "SOP"]

def show():
    st.markdown(
    "<h1 style='text-align: center; color: white;'>Daftar Alat Medis Publik</h1>", 
    unsafe_allow_html=True
)
    try:
        worksheet = open_sheet(SPREADSHEET_ID, "daftar_alat")
    except ValueError:
        create_worksheet_with_header(SPREADSHEET_ID, "daftar_alat", HEADERS)
        worksheet = open_sheet(SPREADSHEET_ID, "daftar_alat")

    data = worksheet.service.spreadsheets().values().get(
        spreadsheetId=worksheet.spreadsheet_id,
        range=f"{worksheet.worksheet_name}!A1:Z1000"
    ).execute().get('values', [])

    if len(data) <= 1:
        st.info("Belum ada alat medis terdaftar.")
    else:
        df = pd.DataFrame(data[1:], columns=data[0])
        st.dataframe(df)

    st.subheader("Tambah Alat Baru")
    with st.form("form_tambah_alat"):
        nama_alat = st.text_input("NAMA ALAT")
        no_sn = st.text_input("NO SN")
        merk = st.text_input("MERK")
        tipe = st.text_input("TIPE")
        ruangan = st.text_input("RUANGAN")
        sop = st.text_area("SOP")

        submitted = st.form_submit_button("Tambah")

        if submitted:
            if not nama_alat:
                st.error("NAMA ALAT harus diisi.")
            else:
                row = [nama_alat, no_sn, merk, tipe, ruangan, sop]
                worksheet.append_row(row)
                st.success(f"Alat {nama_alat} berhasil ditambahkan.")
