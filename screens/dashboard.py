import streamlit as st
import pandas as pd
import plotly.express as px
from gsheets_helper import open_sheet

# ID Google Sheets
SPREADSHEET_ID_ALAT = "1pONEpw-ww19dOJ88vibUTuBy6PvMOBTso7Yp2LVbjAU"       # untuk daftar_alat
SPREADSHEET_ID_MAINT = "1sELnjwsgObSAtfAf2tGZSGvj47dfYC1ESDZSaXqTN4g"       # untuk input_maintenance

def show():
    # Judul Dashboard
    st.markdown(
        "<h1 style='text-align: center; color: white;'>📊 Dashboard Alat Medis</h1>", 
        unsafe_allow_html=True
    )

    # --- Load Data dari Google Sheet ---

    # Daftar Alat
    try:
        df_alat_raw = open_sheet(SPREADSHEET_ID_ALAT, "daftar_alat").service.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID_ALAT,
            range="daftar_alat!A1:Z1000"
        ).execute().get("values", [])
        if len(df_alat_raw) > 1:
            df_alat = pd.DataFrame(df_alat_raw[1:], columns=df_alat_raw[0])
        else:
            df_alat = pd.DataFrame(columns=["NAMA ALAT", "RUANGAN", "MERK"])
    except Exception:
        df_alat = pd.DataFrame(columns=["NAMA ALAT", "RUANGAN", "MERK"])

    # Maintenance
    try:
        df_maint_raw = open_sheet(SPREADSHEET_ID_MAINT, "input_maintenance").service.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID_MAINT,
            range="input_maintenance!A1:Z1000"
        ).execute().get("values", [])
        if len(df_maint_raw) > 1:
            df_maint = pd.DataFrame(df_maint_raw[1:], columns=df_maint_raw[0])
        else:
            df_maint = pd.DataFrame(columns=["Tanggal", "Ruangan", "Nama Alat", "Nama Teknisi", "Status", "Catatan", "Gambar"])
    except Exception:
        df_maint = pd.DataFrame(columns=["Tanggal", "Ruangan", "Nama Alat", "Nama Teknisi", "Status", "Catatan", "Gambar"])

    # Format tanggal di maintenance jika ada datanya
    if "Tanggal" in df_maint.columns and not df_maint.empty:
        df_maint["Tanggal"] = pd.to_datetime(df_maint["Tanggal"], errors="coerce")

    # --- Statistik Umum ---
    st.subheader("📌 Statistik Umum")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Alat", len(df_alat))
    col2.metric("Total Maintenance", len(df_maint))
    col3.metric("Jumlah Ruangan", df_alat["RUANGAN"].nunique() if "RUANGAN" in df_alat else 0)

    # --- Distribusi Alat per Ruangan ---
    st.subheader("📍 Distribusi Alat per Ruangan")
    if not df_alat.empty and "RUANGAN" in df_alat.columns:
        fig = px.histogram(df_alat, x="RUANGAN", title="Jumlah Alat per Ruangan")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Tidak ada data ruangan untuk ditampilkan.")

    # --- Riwayat Maintenance Terbaru ---
    st.subheader("🛠️ Riwayat Maintenance Terbaru")
    if not df_maint.empty:
        df_maint = df_maint.dropna(subset=['Tanggal'])
        df_recent = df_maint.sort_values("Tanggal", ascending=False).head(10)
        df_recent['Tanggal'] = df_recent['Tanggal'].dt.strftime('%d-%m-%Y')
        st.dataframe(df_recent)
    else:
        st.info("Belum ada data maintenance.")

    # --- Notifikasi Alat Rusak ---
    st.subheader("⚠️ Notifikasi Alat Rusak")
    if not df_maint.empty and "Status" in df_maint.columns:
        df_maint["Status"] = df_maint["Status"].fillna("")
        rusak = df_maint[df_maint["Status"].str.lower() == "rusak"]
        if not rusak.empty:
            st.error(f"{len(rusak)} alat dalam kondisi Rusak!")
            st.dataframe(rusak[["Tanggal", "Ruangan", "Nama Alat", "Status"]])
        else:
            st.success("Semua alat dalam kondisi baik.")
    else:
        st.info("Semua alat dalam kondisi baik.")
