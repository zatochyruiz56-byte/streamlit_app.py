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
    .stButton>button { background-color: #6c5ce7 !important; color: white !important; width: 100%; border: none; height: 45px; margin-top: 10px; }
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

# --- FUNCIONES DE ENVÍO DE CORREO ---
def send_otp_email(target_email, code):
    url = "https://api.resend.com/emails"
    headers = {
        "Authorization": f"Bearer {st.secrets['resend_api_key']}",
        "Content-Type": "application/json"
    }
    data = {
        "from": "ZTCHY PRO <onboarding@resend.dev>",
        "to": target_email,
        "subject": "Tu código de verificación ZTCHY",
        "html": f"""
        <div style="font-family: sans-serif; text-align: center;">
            <h2>Confirma tu registro en ZTCHY-PRO</h2>
            <p>Tu código de verificación es:</p>
            <h1 style="color: #6c5ce7; font-size: 40px;">{code}</h1>
            <p>Copia este código y pégalo en la aplicación.</p>
        </div>
        """
    }
    return requests.post(url, headers=headers, json=data)

# --- LÓGICA DE ESTADO ---
if "view" not in st.session_state: st.session_state.view = "login"
if "otp_code" not in st.session_state: st.session_state.otp_code = None
if "temp_user" not in st.session_state: st.session_state.temp_user = {}

st.markdown('<div class="auth-card">', unsafe_allow_html=True)

# --- VISTA: LOGIN ---
if st.session_state.view == "login":
    st.markdown("<h2>Iniciar Sesión</h2>", unsafe_allow_html=True)
    user_email = st.text_input("Correo")
    user_pass = st.text_input("Contraseña", type="password")
    
    if st.button("INGRESAR"):
        try:
            # En Firebase Admin comprobamos si el usuario existe
            auth.get_user_by_email(user_email)
            st.success("¡Bienvenido!")
            st.balloons()
        except:
            st.error("Usuario no registrado o datos incorrectos.")
            
    if st.button("Crear Cuenta"):
        st.session_state.view = "register"
        st.rerun()

# --- VISTA: REGISTRO ---
elif st.session_state.view == "register":
    st.markdown("<h2>Nueva Cuenta</h2>", unsafe_allow_html=True)
    reg_email = st.text_input("Correo Real")
    reg_pass = st.text_input("Contraseña (mínimo 6)", type="password")
    
    if st.button("ENVIAR CÓDIGO"):
        if len(reg_pass) < 6:
            st.warning("La contraseña debe ser de al menos 6 caracteres.")
        elif "@" not in reg_email:
            st.error("Ingresa un correo válido.")
        else:
            # Generamos el código
            st.session_state.otp_code = str(random.randint(100000, 999999))
            st.session_state.temp_user = {"email": reg_email, "pass": reg_pass}
            
            # Enviamos vía Resend
            with st.spinner("Enviando código..."):
                response = send_otp_email(reg_email, st.session_state.otp_code)
                if response.status_code in [200, 201]:
                    st.success("¡Código enviado! Revisa tu bandeja de entrada.")
                    st.session_state.view = "verify"
                    st.rerun()
                else:
                    st.error(f"Error al enviar: {response.text}")

    if st.button("Volver"):
        st.session_state.view = "login"
        st.rerun()

# --- VISTA: VERIFICACIÓN ---
elif st.session_state.view == "verify":
    st.markdown("<h2>Verificar Código</h2>", unsafe_allow_html=True)
    st.write(f"Código enviado a: **{st.session_state.temp_user.get('email')}**")
    input_code = st.text_input("Ingresa los 6 dígitos")
    
    if st.button("ACTIVAR CUENTA"):
        if input_code == st.session_state.otp_code:
            try:
                # CREACIÓN REAL EN FIREBASE
                auth.create_user(
                    email=st.session_state.temp_user['email'],
                    password=st.session_state.temp_user['pass']
                )
                st.success("✅ ¡Cuenta activada con éxito!")
                st.session_state.view = "login"
                st.rerun()
            except Exception as e:
                st.error(f"Error creando el usuario: {e}")
        else:
            st.error("Código incorrecto.")

st.markdown('</div>', unsafe_allow_html=True)
