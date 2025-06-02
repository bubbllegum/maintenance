import streamlit as st
from datetime import datetime
import requests

TELEGRAM_BOT_TOKEN = "8090603259:AAE_heFdrv5Zweird0HVuGHroJSHnF7Hp1k"
TELEGRAM_CHAT_ID = "7101713003"

def kirim_notif_telegram(teks, foto=None):
    url_base = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"
    if foto:
        files = {'photo': foto}
        data = {'chat_id': TELEGRAM_CHAT_ID, 'caption': teks}
        response = requests.post(f"{url_base}/sendPhoto", data=data, files=files)
    else:
        data = {'chat_id': TELEGRAM_CHAT_ID, 'text': teks, 'parse_mode': 'Markdown'}
        response = requests.post(f"{url_base}/sendMessage", data=data)
    return response.json()

def show():
    st.title("Laporan Kerusakan Alat Medis (Publik)")

    nama_pelapor = st.text_input("Nama Pelapor")
    alat_terkait = st.text_input("Alat Terkait")
    keterangan = st.text_area("Keterangan Kerusakan")
    foto = st.file_uploader("Upload Foto Bukti Kerusakan (jpg/png)", type=['jpg', 'jpeg', 'png'])

    if st.button("Kirim Laporan"):
        if not alat_terkait or not keterangan:
            st.error("Alat Terkait dan Keterangan Kerusakan wajib diisi.")
            return

        teks = f"*Laporan Kerusakan Baru*\n\n" \
               f"Pelapor: {nama_pelapor or '-'}\n" \
               f"Alat: {alat_terkait}\n" \
               f"Keterangan: {keterangan}\n" \
               f"Waktu: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

        if foto:
            # Kirim foto dengan caption
            result = kirim_notif_telegram(teks, foto)
        else:
            # Kirim pesan teks saja
            result = kirim_notif_telegram(teks)

        if result.get("ok"):
            st.success("Laporan berhasil dikirim ke Telegram!")
        else:
            st.error(f"Gagal mengirim laporan: {result}")

