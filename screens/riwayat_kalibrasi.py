import streamlit as st
import pandas as pd
from gsheets_helper import open_sheet

SPREADSHEET_ID = "1kSKQkC_53YkZSpcZejXEdRuKLoJwOow10oLZvUs46ac"

@st.cache_data(ttl=600)
def load_data(sheet_name):
    try:
        worksheet = open_sheet(SPREADSHEET_ID, sheet_name)
        data = worksheet.service.spreadsheets().values().get(
            spreadsheetId=worksheet.spreadsheet_id,
            range=f"{worksheet.worksheet_name}!A1:Z1000"
        ).execute().get('values', [])
        if len(data) <= 1:
            return pd.DataFrame()
        df = pd.DataFrame(data[1:], columns=data[0])

        # Format tanggal jika ada kolom TANGGAL_KALIBRASI_TERAKHIR
        if 'TANGGAL_KALIBRASI_TERAKHIR' in df.columns:
            df['TANGGAL_KALIBRASI_TERAKHIR'] = pd.to_datetime(df['TANGGAL_KALIBRASI_TERAKHIR'], errors='coerce').dt.strftime('%Y-%m-%d')
        return df
    except Exception as e:
        st.error(f"Gagal memuat data {sheet_name}: {e}")
        return pd.DataFrame()

def show():
    st.markdown(
    "<h1 style='text-align: center; color: white;'>Riwayat kalibrasi internal dan eksternal</h1>", 
    unsafe_allow_html=True
)
    st.subheader("Kalibrasi Internal")
    df_internal = load_data("kalibrasi_internal")
    if df_internal.empty:
        st.info("Data kalibrasi internal belum tersedia.")
    else:
        st.dataframe(df_internal)

    st.subheader("Kalibrasi Eksternal")
    df_eksternal = load_data("kalibrasi_eksternal")
    if df_eksternal.empty:
        st.info("Data kalibrasi eksternal belum tersedia.")
    else:
        st.dataframe(df_eksternal)
