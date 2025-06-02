import streamlit as st

def show():
    st.markdown(
    "<h1 style='text-align: center; color: white;'>Manual Teknisi</h1>", 
    unsafe_allow_html=True
)
    st.write("Dokumentasi teknis, troubleshooting, dan FAQ untuk teknisi.")

    st.markdown("""
    ### Troubleshooting ECG 001
    - Pastikan kabel terhubung dengan baik
    - Lakukan kalibrasi ulang jika hasil tidak stabil

    ### FAQ
    1. Bagaimana cara reset alat?  
       Tekan tombol reset selama 5 detik.

    2. Siapa yang harus dihubungi jika terjadi kerusakan?  
       Hubungi bagian maintenance.

    ### Video Tutorial  
    [Lihat video tutorial ECG 001](https://www.youtube.com/watch?v=dQw4w9WgXcQ)
    """)
