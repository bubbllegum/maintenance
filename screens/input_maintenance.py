import streamlit as st
from gsheets_helper import open_sheet, create_worksheet
from googleapiclient.errors import HttpError
import base64

SPREADSHEET_ID = "1sELnjwsgObSAtfAf2tGZSGvj47dfYC1ESDZSaXqTN4g"

def show():
    st.markdown(
    "<h1 style='text-align: center; color: white;'>Input Maintenance</h1>", 
    unsafe_allow_html=True
)
    st.write("Masukkan data maintenance alat dan simpan ke Google Sheets.")

    with st.form("maintenance_form"):
        tanggal = st.date_input("Tanggal Maintenance")
        ruangan = st.text_input("Ruangan", "")  # Input ruangan
        alat = st.text_input("Nama Alat", "")
        teknisi = st.text_input("Nama Teknisi", "")
        status = st.selectbox("Status", ["Selesai", "Perbaikan", "Dalam Proses"])
        catatan = st.text_area("Catatan")
        gambar = st.file_uploader("Upload Gambar (opsional)", type=["png", "jpg", "jpeg"])

        submitted = st.form_submit_button("Simpan")

        if submitted:
            # Encode gambar ke base64 jika ada
            if gambar is not None:
                gambar_bytes = gambar.read()
                gambar_base64 = base64.b64encode(gambar_bytes).decode('utf-8')
            else:
                gambar_base64 = ""

            try:
                worksheet_name = f"{ruangan} - {alat}"
                try:
                    worksheet_alat = open_sheet(SPREADSHEET_ID, worksheet_name)
                except ValueError:
                    create_worksheet(SPREADSHEET_ID, worksheet_name)
                    worksheet_alat = open_sheet(SPREADSHEET_ID, worksheet_name)

                row = [str(tanggal), ruangan, alat, teknisi, status, catatan, gambar_base64]
                worksheet_alat.append_row(row)
                st.success(f"Data maintenance berhasil disimpan di worksheet '{worksheet_name}'!")
            except Exception as e:
                st.error(f"Terjadi kesalahan: {e}")
