import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth
import requests
import random

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="ZTCHY-PRO", page_icon="🛡️")

# --- ESTILO VISUAL ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), 
                    url('https://images.unsplash.com/photo-1526392060635-9d6019884377?q=80&w=2070');
        background-size: cover;
    }
    .auth-card {
        background-color: white !important;
        padding: 40px;
        border-radius: 15px;
        color: black !important;
        max-width: 500px;
        margin: auto;
    }
    h2, label, p { color: black !important; font-weight: bold !important; }
    .stButton>button { background-color: #6c5ce7 !important; color: white !important; width: 100%; border: none; height: 45px; }
    </style>
    """, unsafe_allow_html=True)

# --- INICIALIZACIÓN DE FIREBASE ---
if not firebase_admin._apps:
    try:
        private_key = st.secrets["firebase"]["private_key"].replace('\\n', '\n')
        fb_credentials = {
            "type": st.secrets["firebase"]["type"],
            "project_id": st.secrets["firebase"]["project_id"],
            "private_key_id": st.secrets["firebase"]["private_key_id"],
            "private_key": private_key,
            "client_email": st.secrets["firebase"]["client_email"],
            "client_id": st.secrets["firebase"]["client_id"],
            "auth_uri": st.secrets["firebase"]["auth_uri"],
            "token_uri": st.secrets["firebase"]["token_uri"],
            "auth_provider_x509_cert_url": st.secrets["firebase"]["auth_provider_x509_cert_url"],
            "client_x509_cert_url": st.secrets["firebase"]["client_x509_cert_url"]
        }
        cred = credentials.Certificate(fb_credentials)
        firebase_admin.initialize_app(cred)
    except Exception as e:
        st.error(f"Error de Firebase: {e}")

# --- FUNCIONES DE APOYO ---
def send_otp_email(target_email, code):
    """Envía el código de 6 dígitos usando la API de Resend"""
    url = "https://api.resend.com/emails"
    headers = {
        "Authorization": f"Bearer {st.secrets['resend_api_key']}",
        "Content-Type": "application/json"
    }
    data = {
        "from": "ZTCHY PRO <onboarding@resend.dev>",
        "to": target_email,
        "subject": "Tu código de verificación ZTCHY",
        "html": f"<h2>Confirma tu registro</h2><p>Tu código de verificación es:</p><h1>{code}</h1>"
    }
    return requests.post(url, headers=headers, json=data)

# --- LÓGICA DE NAVEGACIÓN ---
if "view" not in st.session_state: st.session_state.view = "login"
if "otp_code" not in st.session_state: st.session_state.otp_code = None
if "temp_user" not in st.session_state: st.session_state.temp_user = {}

st.markdown('<div class="auth-card">', unsafe_allow_html=True)

# VISTA: LOGIN
if st.session_state.view == "login":
    st.markdown("<h2>Iniciar Sesión</h2>", unsafe_allow_html=True)
    user_email = st.text_input("Correo Electrónico")
    user_pass = st.text_input("Contraseña", type="password")
    
    if st.button("INGRESAR"):
        try:
            auth.get_user_by_email(user_email)
            st.success("¡Acceso concedido!")
            st.balloons()
        except:
            st.error("Usuario no encontrado.")
            
    if st.button("¿No tienes cuenta? Regístrate"):
        st.session_state.view = "register"
        st.rerun()

# VISTA: REGISTRO
elif st.session_state.view == "register":
    st.markdown("<h2>Crear Nueva Cuenta</h2>", unsafe_allow_html=True)
    reg_email = st.text_input("Email")
    reg_pass = st.text_input("Contraseña (min. 6)", type="password")
    
    if st.button("ENVIAR CÓDIGO"):
        if len(reg_pass) < 6:
            st.warning("Contraseña muy corta.")
        else:
            # Generamos código y guardamos datos temporalmente
            st.session_state.otp_code = str(random.randint(100000, 999999))
            st.session_state.temp_user = {"email": reg_email, "pass": reg_pass}
            
            # Enviamos el correo
            response = send_otp_email(reg_email, st.session_state.otp_code)
            if response.status_code == 201 or response.status_code == 200:
                st.success("¡Código enviado! Revisa tu correo.")
                st.session_state.view = "verify"
                st.rerun()
            else:
                st.error("Error enviando el correo. Verifica tu API Key de Resend.")

    if st.button("Volver"):
        st.session_state.view = "login"
        st.rerun()

# VISTA: VERIFICACIÓN OTP
elif st.session_state.view == "verify":
    st.markdown("<h2>Verificar Código</h2>", unsafe_allow_html=True)
    st.write(f"Enviamos un código a: {st.session_state.temp_user['email']}")
    input_code = st.text_input("Ingresa los 6 dígitos")
    
    if st.button("CONFIRMAR"):
        if input_code == st.session_state.otp_code:
            try:
                # Si el código es correcto, recién ahí lo creamos en Firebase
                auth.create_user(
                    email=st.session_state.temp_user['email'],
                    password=st.session_state.temp_user['pass']
                )
                st.success("✅ ¡Cuenta verificada y creada!")
                st.session_state.view = "login"
                st.rerun()
            except Exception as e:
                st.error(f"Error al crear usuario: {e}")
        else:
            st.error("Código incorrecto.")

st.markdown('</div>', unsafe_allow_html=True)
