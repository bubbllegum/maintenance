import streamlit as st
import base64
import time
from gsheets_helper import (
    open_sheet, 
    create_worksheet_with_header, 
    worksheet_exists
)

SPREADSHEET_ID = "1sELnjwsgObSAtfAf2tGZSGvj47dfYC1ESDZSaXqTN4g"

def show():
    st.markdown(
        "<h1 style='text-align: center; color: white;'>Input Maintenance</h1>",
        unsafe_allow_html=True,
    )
    st.write("Masukkan data maintenance alat dan simpan ke Google Sheets.")

    with st.form("maintenance_form"):
        tanggal = st.date_input("Tanggal Maintenance")
        ruangan = st.text_input("Ruangan", "")
        alat = st.text_input("Nama Alat", "")
        teknisi = st.text_input("Nama Teknisi", "")
        status = st.selectbox("Status", ["Selesai", "Perbaikan", "Dalam Proses"])
        catatan = st.text_area("Catatan")
        gambar = st.file_uploader("Upload Gambar (opsional)", type=["png", "jpg", "jpeg"])

        submitted = st.form_submit_button("Simpan")

        if submitted:
            if not ruangan or not alat:
                st.error("Ruangan dan Nama Alat harus diisi!")
                st.stop()

            if gambar is not None:
                gambar_bytes = gambar.read()
                gambar_base64 = base64.b64encode(gambar_bytes).decode("utf-8")
            else:
                gambar_base64 = ""

            worksheet_name = f"{ruangan} - {alat}"
            headers = ["Tanggal", "Ruangan", "Alat", "Teknisi", "Status", "Catatan", "Gambar (Base64)"]

            if worksheet_exists(SPREADSHEET_ID, worksheet_name):
                worksheet_alat = open_sheet(SPREADSHEET_ID, worksheet_name)
            else:
                try:
                    create_worksheet_with_header(SPREADSHEET_ID, worksheet_name, headers)
                    time.sleep(2)  # Tunggu sheet siap
                    worksheet_alat = open_sheet(SPREADSHEET_ID, worksheet_name)
                except Exception as e:
                    st.error(f"Gagal membuat worksheet baru: {e}")
                    st.stop()

            try:
                row = [
                    str(tanggal),
                    ruangan,
                    alat,
                    teknisi,
                    status,
                    catatan,
                    gambar_base64,
                ]
                worksheet_alat.append_row(row)
                st.success(f"Data berhasil disimpan di worksheet '{worksheet_name}'!")
            except Exception as e:
                st.error(f"Gagal menambahkan data: {e}")
