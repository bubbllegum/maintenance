import streamlit as st
import pandas as pd
import plotly.express as px
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# Path ke file credential JSON Google service account kamu
SERVICE_ACCOUNT_FILE = "credentials.json"

# Scope akses spreadsheet readonly
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# ID Google Sheets
SPREADSHEET_ID_ALAT = "1pONEpw-ww19dOJ88vibUTuBy6PvMOBTso7Yp2LVbjAU"       # daftar alat
SPREADSHEET_ID_MAINT = "1sELnjwsgObSAtfAf2tGZSGvj47dfYC1ESDZSaXqTN4g"     # input maintenance

def get_service():
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=creds)
    return service

def load_maintenance_all_sheets(spreadsheet_id):
    try:
        service = get_service()
        spreadsheet = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
        sheet_titles = [sheet['properties']['title'] for sheet in spreadsheet.get('sheets', [])]
        st.write(f"Worksheet ditemukan: {sheet_titles}")

        all_data = []
        for title in sheet_titles:
            result = service.spreadsheets().values().get(
                spreadsheetId=spreadsheet_id,
                range=f"'{title}'!A1:Z1000"
            ).execute()
            values = result.get('values', [])
            st.write(f"{title} punya {len(values)-1} data baris")
            if len(values) > 1:
                df = pd.DataFrame(values[1:], columns=values[0])
                all_data.append(df)

        if all_data:
            df_all = pd.concat(all_data, ignore_index=True)
            st.write(f"Total baris maintenance gabungan: {len(df_all)}")
            return df_all
        else:
            st.info("Tidak ada data maintenance di semua worksheet.")
            return pd.DataFrame(columns=["Tanggal", "Ruangan", "Nama Alat", "Nama Teknisi", "Status", "Catatan", "Gambar"])

    except Exception as e:
        st.error(f"Error load maintenance: {e}")
        return pd.DataFrame(columns=["Tanggal", "Ruangan", "Nama Alat", "Nama Teknisi", "Status", "Catatan", "Gambar"])

def show():
    st.markdown("<h1 style='text-align: center; color: white;'>📊 Dashboard Alat Medis</h1>", unsafe_allow_html=True)

    # Load daftar alat
    try:
        service = get_service()
        result = service.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID_ALAT,
            range="daftar_alat!A1:Z1000"
        ).execute()
        values = result.get('values', [])
        if len(values) > 1:
            df_alat = pd.DataFrame(values[1:], columns=values[0])
            df_alat.columns = df_alat.columns.str.upper()
        else:
            df_alat = pd.DataFrame(columns=["NAMA ALAT", "RUANGAN", "MERK"])
    except Exception as e:
        st.error(f"Gagal load daftar alat: {e}")
        df_alat = pd.DataFrame(columns=["NAMA ALAT", "RUANGAN", "MERK"])

    # Load maintenance gabungan
    df_maint = load_maintenance_all_sheets(SPREADSHEET_ID_MAINT)

    # Normalisasi nama kolom di maintenance
    df_maint.columns = df_maint.columns.str.capitalize()

    # Format tanggal
    if "Tanggal" in df_maint.columns and not df_maint.empty:
        df_maint["Tanggal"] = pd.to_datetime(df_maint["Tanggal"], errors="coerce")

    # Statistik umum
    st.subheader("📌 Statistik Umum")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Alat", len(df_alat))
    col2.metric("Total Maintenance", len(df_maint))
    col3.metric("Jumlah Ruangan", df_alat["RUANGAN"].nunique() if "RUANGAN" in df_alat.columns else 0)

    # Distribusi alat per ruangan
    st.subheader("📍 Distribusi Alat per Ruangan")
    if not df_alat.empty and "RUANGAN" in df_alat.columns:
        fig = px.histogram(df_alat, x="RUANGAN", title="Jumlah Alat per Ruangan")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Tidak ada data ruangan untuk ditampilkan.")

    # Riwayat maintenance terbaru
    st.subheader("🛠️ Riwayat Maintenance Terbaru")
    if not df_maint.empty:
        df_recent = df_maint.sort_values("Tanggal", ascending=False).head(10)
        st.dataframe(df_recent)
    else:
        st.info("Belum ada data maintenance.")

    # Notifikasi alat rusak
    st.subheader("⚠️ Notifikasi Alat Rusak")
    if not df_maint.empty and "Status" in df_maint.columns:
        df_maint["Status"] = df_maint["Status"].fillna("")
        rusak = df_maint[df_maint["Status"].str.lower() == "rusak"]
        if not rusak.empty:
            st.error(f"{len(rusak)} alat dalam kondisi rusak!")
            st.dataframe(rusak[["Tanggal", "Ruangan", "Nama Alat", "Status"]])
        else:
            st.success("Semua alat dalam kondisi baik.")
    else:
        st.info("Semua alat dalam kondisi baik.")
