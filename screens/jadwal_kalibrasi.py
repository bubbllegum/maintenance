import streamlit as st
import pandas as pd
from datetime import datetime
from gsheets_helper import open_sheet, create_worksheet_with_header
import requests

SPREADSHEET_ID = "1kSKQkC_53YkZSpcZejXEdRuKLoJwOow10oLZvUs46ac"
TELEGRAM_BOT_TOKEN = "8099484179:AAGXn3mJEvTTOSOBj1T67SOQHTY2nkPs7Uc"
TELEGRAM_CHAT_ID = "7101713003"

HEADERS = [
    "NAMA ALAT",
    "NO SN",
    "TIPE",
    "RUANGAN",
    "TANGGAL MULAI",
    "TANGGAL_KALIBRASI_TERAKHIR",
    "INTERVAL_HARI"
]

def kirim_notif_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/Perlu di kalibrasi"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    response = requests.post(url, data=payload)
    return response.json()

def pastikan_worksheet(sheet_name):
    try:
        open_sheet(SPREADSHEET_ID, sheet_name)
    except ValueError:
        create_worksheet_with_header(SPREADSHEET_ID, sheet_name, HEADERS)

def load_data(sheet_name):
    try:
        worksheet = open_sheet(SPREADSHEET_ID, sheet_name)
        data = worksheet.service.spreadsheets().values().get(
            spreadsheetId=worksheet.spreadsheet_id,
            range=f"{worksheet.worksheet_name}!A1:Z1000"
        ).execute().get('values', [])
        if len(data) <= 1:
            return pd.DataFrame(columns=HEADERS)
        return pd.DataFrame(data[1:], columns=data[0])
    except Exception:
        return pd.DataFrame(columns=HEADERS)

def simpan_data(sheet_name, row):
    worksheet = open_sheet(SPREADSHEET_ID, sheet_name)
    worksheet.append_row(row)

def cek_dan_kirim_notif(df, sheet_name):
    today = pd.to_datetime(datetime.now().date())
    df['TANGGAL_KALIBRASI_TERAKHIR'] = pd.to_datetime(df['TANGGAL_KALIBRASI_TERAKHIR'], errors='coerce')
    df['INTERVAL_HARI'] = pd.to_numeric(df['INTERVAL_HARI'], errors='coerce').fillna(180).astype(int)
    df['TANGGAL_KALIBRASI_BERIKUTNYA'] = df['TANGGAL_KALIBRASI_TERAKHIR'] + pd.to_timedelta(df['INTERVAL_HARI'], unit='d')

    def status_kalibrasi(next_date):
        if pd.isna(next_date):
            return "Tanggal tidak valid"
        elif next_date < today:
            return "Terlambat"
        else:
            return "Akan datang"

    df['STATUS'] = df['TANGGAL_KALIBRASI_BERIKUTNYA'].apply(status_kalibrasi)

    terlambat = df[df['STATUS'] == 'Terlambat']

    for _, row in terlambat.iterrows():
        pesan = (
            f"*Pengingat Kalibrasi {sheet_name.replace('_', ' ').title()}:*\n"
            f"Alat: {row['NAMA ALAT']} (SN: {row['NO SN']})\n"
            f"Ruangan: {row['RUANGAN']}\n"
            f"Mulai: {row.get('TANGGAL_MULAI', 'N/A')}\n"
            f"Kalibrasi terakhir: {row['TANGGAL_KALIBRASI_TERAKHIR'].date()}\n"
            f"Kalibrasi berikutnya sudah lewat tanggal {row['TANGGAL_KALIBRASI_BERIKUTNYA'].date()}\n"
            f"Segera lakukan kalibrasi."
        )
        kirim_notif_telegram(pesan)
        st.success(f"Notifikasi Telegram dikirim untuk alat {row['NAMA ALAT']} ({sheet_name})")

def show():
    st.markdown(
    "<h1 style='text-align: center; color: white;'>Jadwal Kalibrasi Internal & Eksternal</h1>", 
    unsafe_allow_html=True
)

    for sheet_name in ['kalibrasi_internal', 'kalibrasi_eksternal']:
        pastikan_worksheet(sheet_name)

    st.subheader("Data Kalibrasi Internal")
    df_internal = load_data("kalibrasi_internal")
    st.dataframe(df_internal)

    st.subheader("Tambah Data Kalibrasi Internal")
    with st.form("form_tambah_internal"):
        nama_alat = st.text_input("Nama Alat (Internal)")
        no_sn = st.text_input("No SN (Internal)")
        tipe = st.text_input("Tipe Alat (Internal)")
        ruangan = st.text_input("Ruangan (Internal)")
        tanggal_mulai = st.date_input("Tanggal Mulai (Internal)")
        tanggal_terakhir = st.date_input("Tanggal Kalibrasi Terakhir (Internal)")
        interval = st.number_input("Interval Kalibrasi (hari)", min_value=1, value=180)
        submitted = st.form_submit_button("Tambah Internal")

        if submitted:
            if not nama_alat or not no_sn:
                st.error("Nama Alat dan No SN wajib diisi.")
            else:
                row = [
                    nama_alat,
                    no_sn,
                    tipe,
                    ruangan,
                    tanggal_mulai.strftime("%Y-%m-%d"),
                    tanggal_terakhir.strftime("%Y-%m-%d"),
                    interval
                ]
                simpan_data("kalibrasi_internal", row)
                st.success(f"Data kalibrasi internal untuk '{nama_alat}' berhasil ditambahkan.")

    st.markdown("---")

    st.subheader("Data Kalibrasi Eksternal")
    df_eksternal = load_data("kalibrasi_eksternal")
    st.dataframe(df_eksternal)

    st.subheader("Tambah Data Kalibrasi Eksternal")
    with st.form("form_tambah_eksternal"):
        nama_alat = st.text_input("Nama Alat (Eksternal)")
        no_sn = st.text_input("No SN (Eksternal)")
        tipe = st.text_input("Tipe Alat (Eksternal)")
        ruangan = st.text_input("Ruangan (Eksternal)")
        tanggal_mulai = st.date_input("Tanggal Mulai (Eksternal)")
        tanggal_terakhir = st.date_input("Tanggal Kalibrasi Terakhir (Eksternal)")
        interval = st.number_input("Interval Kalibrasi (hari)", min_value=1, value=365)
        submitted = st.form_submit_button("Tambah Eksternal")

        if submitted:
            if not nama_alat or not no_sn:
                st.error("Nama Alat dan No SN wajib diisi.")
            else:
                row = [
                    nama_alat,
                    no_sn,
                    tipe,
                    ruangan,
                    tanggal_mulai.strftime("%Y-%m-%d"),
                    tanggal_terakhir.strftime("%Y-%m-%d"),
                    interval
                ]
                simpan_data("kalibrasi_eksternal", row)
                st.success(f"Data kalibrasi eksternal untuk '{nama_alat}' berhasil ditambahkan.")
