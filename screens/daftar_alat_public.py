import streamlit as st
from gsheets_helper import open_sheet
import pandas as pd

SPREADSHEET_ID = "1pONEpw-ww19dOJ88vibUTuBy6PvMOBTso7Yp2LVbjAU"

def show():
    st.markdown(
    "<h1 style='text-align: center; color: white;'>Daftar Alat Medis</h1>", 
    unsafe_allow_html=True
)

    try:
        worksheet = open_sheet(SPREADSHEET_ID, "daftar_alat")
        data = worksheet.service.spreadsheets().values().get(
            spreadsheetId=worksheet.spreadsheet_id,
            range=f"{worksheet.worksheet_name}!A1:Z1000"
        ).execute().get('values', [])
    except Exception as e:
        st.error(f"Gagal mengambil data: {e}")
        return

    if len(data) <= 1:
        st.info("Belum ada alat medis terdaftar.")
        return

    df = pd.DataFrame(data[1:], columns=data[0])

    st.subheader("Pilih Alat untuk melihat SOP")

    selected_index = st.selectbox(
        "Nama Alat",
        df.index,
        format_func=lambda i: df.loc[i, "NAMA ALAT"]
    )

    selected_alat = df.loc[selected_index, "NAMA ALAT"]
    sop = df.loc[selected_index, "SOP"]

    st.markdown(f"### SOP untuk: {selected_alat}")

    if sop.strip() == "":
        st.info("SOP belum tersedia untuk alat ini.")
    else:
        st.markdown(f'<div class="glowing-box">{sop}</div>', unsafe_allow_html=True)
