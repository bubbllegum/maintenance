import os
import io
import streamlit as st
import yaml
from yaml.loader import SafeLoader
import bcrypt
from streamlit_option_menu import option_menu

# Buat file credentials.json dari secret ENV VAR jika belum ada
credential_json_str = os.getenv("CREDENTIALS_JSON")
if credential_json_str and not os.path.exists("credentials.json"):
    with open("credentials.json", "w") as f:
        f.write(credential_json_str)

# Load credentials.yaml dari secret ENV VAR atau file fallback
credential_yaml_str = os.getenv("CREDENTIALS_YAML")
if credential_yaml_str:
    config = yaml.load(io.StringIO(credential_yaml_str), Loader=SafeLoader)
else:
    with open('credentials.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)

VALID_USERS = {user['username']: user['password_hash'] for user in config['credentials']}

# Import modul screens
from screens import (
    daftar_alat_public,
    riwayat_kalibrasi,
    laporan_kerusakan,
    dashboard,
    input_maintenance,
    laporan_maintenance,
    daftar_alat,
    jadwal_kalibrasi,
    manual_teknisi,
)

def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())

def do_logout():
    st.session_state['logged_in'] = False
    st.session_state['username'] = None
    st.session_state['input_username'] = ''
    st.session_state['input_password'] = ''
    st.session_state['cookie_expiry_days'] = 0
    st.session_state['remember_me'] = False
    st.session_state['reload'] = not st.session_state.get('reload', False)

def logout():
    st.sidebar.markdown(
        """
        <style>
        .logout-btn > button {
            background-color: #dc2626 !important;
            color: white !important;
            width: 100%;
            padding: 8px 0;
            border-radius: 8px;
            font-weight: bold;
            font-size: 14px;
            border: none;
            cursor: pointer;
        }
        .logout-btn > button:hover {
            background-color: #b91c1c !important;
            color: white !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    with st.sidebar.form("logout_form"):
        logout_btn = st.form_submit_button("Logout", help="Klik untuk logout")
        st.markdown('<div class="logout-btn"></div>', unsafe_allow_html=True)

    if logout_btn:
        do_logout()

def login():
    st.sidebar.markdown(
        """
        <style>
        .sidebar .sidebar-content {
            background: #1f2937;
            padding: 20px 15px;
            border-radius: 10px;
            position: relative;
            overflow: hidden;
            color: #fef3c7;
        }
        .login-header {
            text-align: center;
            margin-bottom: 20px;
            position: relative;
            z-index: 2;
            color: #fef3c7;
        }
        .login-logo {
            display: inline-block;
            margin-bottom: 10px;
            max-width: 140px;
            width: 100%;
            position: relative;
            z-index: 2;
        }
        .fade-text {
            font-family: 'Cursive', sans-serif;
            font-size: 24px;
            animation: fadeIn 3s infinite;
            position: relative;
            z-index: 2;
            color: #fef3c7;
        }
        @keyframes fadeIn {
            0% { opacity: 0; }
            50% { opacity: 1; }
            100% { opacity: 0; }
        }

        /* Kotak bercahaya umum */
        .glowing-box {
            border: 2px solid #fef3c7;
            border-radius: 8px;
            padding: 15px;
            margin: 10px 0;
            background-color: rgba(31, 41, 55, 0.8);
            color: #fef3c7;
            font-weight: 600;
            box-shadow: 0 0 15px 4px #facc15;
            white-space: pre-wrap;
            word-wrap: break-word;
            transition: box-shadow 0.3s ease-in-out;
        }
        .glowing-box:hover {
            box-shadow: 0 0 25px 8px #facc15;
        }
        </style>

        <div class="login-header">
            <img class="login-logo" src="https://i.postimg.cc/gJjQzMxy/IPSSRS.png" alt="Logo">
            <div class="fade-text">🔐 Silakan Login untuk Akses Sistem</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.sidebar.form("login_form"):
        username = st.text_input("Username", value=st.session_state.get('input_username', ''))
        password = st.text_input("Password", type="password", value=st.session_state.get('input_password', ''))
        remember_me = st.checkbox("Remember Me", value=st.session_state.get('remember_me', True))
        st.session_state['remember_me'] = remember_me
        login_btn = st.form_submit_button("Login")

    if login_btn:
        st.session_state['input_username'] = username
        st.session_state['input_password'] = password

        if username in VALID_USERS and verify_password(password, VALID_USERS[username]):
            st.success(f"🎉 Selamat datang, **{username}**!")
            st.session_state['logged_in'] = True
            st.session_state['username'] = username
            st.session_state['cookie_expiry_days'] = 30 if remember_me else 1
            st.session_state['reload'] = not st.session_state.get('reload', False)
        else:
            st.error("⚠️ Username atau password salah. Silakan coba lagi.")

def inject_animations():
    st.markdown(
        """
        <style>
        /* Background gradient full page */
        #animation-container {
            position: fixed;
            top: 0; left: 0;
            width: 100vw;
            height: 100vh;
            pointer-events: none;
            overflow: hidden;
            z-index: 0;
            background: linear-gradient(-45deg, #ff6ec4, #7873f5, #4ade80, #facc15);
            background-size: 400% 400%;
            animation: gradientShift 15s ease infinite;
        }
        @keyframes gradientShift {
            0% {background-position: 0% 50%;}
            50% {background-position: 100% 50%;}
            100% {background-position: 0% 50%;}
        }

        /* Partikel bintang (berpijar) full page */
        .particle {
            position: absolute;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.8);
            box-shadow: 0 0 8px 2px rgba(255, 255, 255, 0.7);
            animation: floatUpDown 6s ease-in-out infinite;
            opacity: 0.8;
            filter: drop-shadow(0 0 6px rgba(255, 255, 255, 0.6));
            pointer-events: none;
        }
        @keyframes floatUpDown {
            0%, 100% { transform: translateY(0) scale(1); opacity: 0.8; }
            50% { transform: translateY(-20px) scale(1.1); opacity: 1; }
        }
        /* Variasi partikel */
        .particle:nth-child(1) {
            width: 12px; height: 12px;
            left: 10%; top: 70%;
            animation-delay: 0s;
        }
        .particle:nth-child(2) {
            width: 8px; height: 8px;
            left: 25%; top: 40%;
            animation-delay: 1.5s;
            animation-duration: 5.5s;
        }
        .particle:nth-child(3) {
            width: 10px; height: 10px;
            left: 50%; top: 80%;
            animation-delay: 3s;
            animation-duration: 6.5s;
        }
        .particle:nth-child(4) {
            width: 7px; height: 7px;
            left: 75%; top: 30%;
            animation-delay: 2s;
            animation-duration: 5s;
        }
        .particle:nth-child(5) {
            width: 9px; height: 9px;
            left: 85%; top: 60%;
            animation-delay: 4s;
            animation-duration: 6s;
        }
        .particle:nth-child(6) {
            width: 6px; height: 6px;
            left: 40%; top: 20%;
            animation-delay: 3.5s;
            animation-duration: 5.2s;
        }
        .particle:nth-child(7) {
            width: 11px; height: 11px;
            left: 60%; top: 50%;
            animation-delay: 1s;
            animation-duration: 6.2s;
        }
        .particle:nth-child(8) {
            width: 5px; height: 5px;
            left: 20%; top: 60%;
            animation-delay: 4.5s;
            animation-duration: 5.7s;
        }

        /* Sidebar styling: teks terang */
        [data-testid="stSidebar"] {
            background-color: #1f2937 !important;
            color: #fef3c7 !important;
            position: relative;  /* agar snow di sidebar bisa absolut */
            overflow: visible !important;
        }
        [data-testid="stSidebar"] * {
            color: #fef3c7 !important;
        }
        [data-testid="stSidebar"] input,
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] button {
            color: #fef3c7 !important;
        }

        /* Container animasi salju di sidebar */
        #sidebar-snow {
            pointer-events: none;
            position: absolute;
            top: 0; left: 0;
            width: 100%;
            height: 100%;
            z-index: 1000;
            overflow: visible;
        }

        /* Salju */
        .snowflake {
            position: absolute;
            top: -10px;
            background: white;
            border-radius: 50%;
            opacity: 0.8;
            filter: drop-shadow(0 0 4px white);
            animation-name: fall, sway;
            animation-timing-function: linear, ease-in-out;
            animation-iteration-count: infinite, infinite;
            pointer-events: none;
        }
        @keyframes fall {
            0% { transform: translateY(0); opacity: 0.8; }
            100% { transform: translateY(120vh); opacity: 0.1; }
        }
        @keyframes sway {
            0%, 100% { transform: translateX(0); }
            50% { transform: translateX(20px); }
        }
        </style>

        <!-- Animasi bintang + gradient warna full page -->
        <div id="animation-container">
            <div class="particle"></div>
            <div class="particle"></div>
            <div class="particle"></div>
            <div class="particle"></div>
            <div class="particle"></div>
            <div class="particle"></div>
            <div class="particle"></div>
            <div class="particle"></div>
        </div>

        <!-- Animasi salju di sidebar -->
        <div id="sidebar-snow"></div>

        <script>
        const snowContainer = document.getElementById('sidebar-snow');
        const snowflakeCount = 30;

        function randomRange(min, max) {
            return Math.random() * (max - min) + min;
        }

        for(let i=0; i<snowflakeCount; i++){
            const snowflake = document.createElement('div');
            snowflake.classList.add('snowflake');
            const size = randomRange(3, 7);
            snowflake.style.width = size + 'px';
            snowflake.style.height = size + 'px';
            snowflake.style.left = Math.random() * 100 + '%';
            snowflake.style.animationDuration = randomRange(5, 10) + 's, ' + randomRange(3, 6) + 's';
            snowflake.style.animationDelay = (Math.random() * 10) + 's, ' + (Math.random() * 10) + 's';
            snowContainer.appendChild(snowflake);
        }
        </script>
        """,
        unsafe_allow_html=True,
    )

# Initialize session state variables
for key, default in {
    'logged_in': False,
    'username': None,
    'input_username': '',
    'input_password': '',
    'remember_me': True,
    'cookie_expiry_days': 0,
    'reload': False
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

authentication_status = st.session_state['logged_in']
name = st.session_state['username'] if authentication_status else None

private_pages = {
    "Dashboard": dashboard.show,
    "Input Maintenance": input_maintenance.show,
    "Laporan Maintenance": laporan_maintenance.show,
    "Daftar Alat": daftar_alat.show,
    "Jadwal Kalibrasi": jadwal_kalibrasi.show,
    "Manual Teknisi": manual_teknisi.show,
}

public_pages = {
    "Dashboard": dashboard.show,
    "Riwayat Kalibrasi internal dan eksternal": riwayat_kalibrasi.show,
    "Daftar Alat": daftar_alat_public.show,
    "Laporan Kerusakan": laporan_kerusakan.show,
}

def main():
    st.set_page_config(page_title="Aplikasi Monitoring", layout="wide")

    inject_animations()

    if not authentication_status:
        login()

    if authentication_status:
        st.sidebar.title(f"Halo, {name} 👋")

        with st.sidebar.expander("Menu Utama", expanded=True):
            private_page = option_menu(
                menu_title=None,
                options=list(private_pages.keys()),
                icons=["speedometer", "gear", "file-earmark-text", "list", "calendar", "book"],
                menu_icon="cast",
                default_index=0,
                orientation="vertical",
            )

        logout()

        private_pages[private_page]()

    else:
        st.sidebar.info("Silakan login terlebih dahulu")

        with st.sidebar.expander("Navigasi Publik", expanded=True):
            public_page = option_menu(
                menu_title=None,
                options=list(public_pages.keys()),
                icons=["speedometer", "clock-history", "list-task", "exclamation-triangle"],
                menu_icon="cast",
                default_index=0,
                orientation="vertical",
            )

        public_pages[public_page]()

        st.sidebar.markdown(
            """
            <style>
            .social-icons {
                text-align: center;
                margin-top: 20px;
            }
            .social-icons a {
                margin: 0 15px;
                display: inline-block;
            }
            .social-icons img {
                display: block;
                margin-left: auto;
                margin-right: auto;
                width: 60px;
                height: 60px;
            }
            </style>
            <div class="social-icons">
                <a href="https://wa.me/085890243536" target="_blank" title="WhatsApp">
                    <img src="https://raw.githubusercontent.com/sahirmaharaj/exifa/main/img/topmate.gif" alt="WhatsApp">
                </a>
                <a href="https://www.instagram.com/oyyrulll" target="_blank" title="Instagram">
                    <img src="https://raw.githubusercontent.com/sahirmaharaj/exifa/main/img/newsletter.gif" alt="Instagram">
                </a>
                <a href="https://mail.google.com/mail/?view=cm&fs=1&to=syahrul.abidin234@gmail.com" target="_blank" title="Email">
                    <img src="https://raw.githubusercontent.com/sahirmaharaj/exifa/main/img/email.gif" alt="Email">
                </a>
            </div>
            """,
            unsafe_allow_html=True,
        )

if __name__ == "__main__":
    main()
