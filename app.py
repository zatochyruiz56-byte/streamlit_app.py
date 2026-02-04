import streamlit as st
from supabase import create_client

# CONFIGURACIÓN VISUAL
st.set_page_config(page_title="ZTCHY-PRO", page_icon="🛡️", layout="centered")

st.markdown("""
    <style>
    header, footer, .stAppDeployButton, #MainMenu {visibility: hidden;}
    [data-testid="stSidebar"] {display: none;}
    
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), 
                    url('https://images.unsplash.com/photo-1526392060635-9d6019884377?q=80&w=2070');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    /* Tarjeta Blanca Sólida - Estilo image_8642bb */
    .auth-card {
        background-color: #ffffff !important;
        padding: 40px;
        border-radius: 20px;
        box-shadow: 0 20px 50px rgba(0,0,0,0.9);
        max-width: 450px;
        margin: auto;
    }

    /* FORZAR TEXTOS EN NEGRO */
    h2, p, label, span, div {
        color: #000000 !important;
        font-weight: 700 !important;
    }
    
    h2 { font-size: 30px; text-align: center; margin-bottom: 25px; }

    /* Inputs Blancos con borde Púrpura */
    .stTextInput input {
        background-color: #ffffff !important;
        border: 2px solid #6c5ce7 !important;
        color: #000000 !important;
        border-radius: 12px !important;
        height: 48px;
    }

    /* Botón Púrpura ZTCHY */
    div.stButton > button {
        background-color: #6c5ce7 !important;
        color: white !important;
        border-radius: 12px !important;
        width: 100%;
        height: 55px;
        font-weight: bold;
        font-size: 18px;
        border: none !important;
        margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# CONEXIÓN SEGURA
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_SECRET_KEY"]
supabase = create_client(url, key)

if "view" not in st.session_state: st.session_state.view = "login"

# LOGO CENTRADO (image_85e4e4)
st.markdown("<div style='text-align: center; margin-bottom: 20px;'><img src='https://i.ibb.co/L9Y0Y5T/Logo-Z.png' width='110'></div>", unsafe_allow_html=True)

st.markdown('<div class="auth-card">', unsafe_allow_html=True)

# VISTA LOGIN
if st.session_state.view == "login":
    st.markdown("<h2>Iniciar Sesión</h2>", unsafe_allow_html=True)
    email = st.text_input("Correo electrónico", key="login_email")
    password = st.text_input("Contraseña", type="password", key="login_pass")
    
    if st.button("INGRESAR"):
        try:
            res = supabase.auth.sign_in_with_password({"email": email, "password": password})
            if res.user: st.success("¡Bienvenido!")
        except: st.error("Acceso denegado. Revisa tus datos.")
    
    if st.button("Crear Cuenta Nueva"):
        st.session_state.view = "register"
        st.rerun()

# VISTA REGISTRO
elif st.session_state.view == "register":
    st.markdown("<h2>Crear Cuenta</h2>", unsafe_allow_html=True)
    reg_mail = st.text_input("Tu Correo Real", key="reg_email")
    reg_pass = st.text_input("Tu Contraseña", type="password", key="reg_pass")
    
    if st.button("COMPLETAR REGISTRO"):
        try:
            # Aquí usamos el SMTP configurado en el paso anterior
            res = supabase.auth.sign_up({"email": reg_mail, "password": reg_pass})
            if res.user:
                st.session_state.temp_email = reg_mail
                st.session_state.view = "verify"
                st.rerun()
        except Exception as e:
            st.error(f"Error: {e}")
            
    if st.button("Volver al Inicio"):
        st.session_state.view = "login"
        st.rerun()

# VISTA VERIFICACIÓN (OTP)
elif st.session_state.view == "verify":
    st.markdown("<h2>Verificación</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center;'>Código enviado a:<br>{st.session_state.temp_email}</p>", unsafe_allow_html=True)
    otp_code = st.text_input("Introduce los 6 dígitos", key="otp_code")
    
    if st.button("ACTIVAR MI CUENTA"):
        try:
            supabase.auth.verify_otp({"email": st.session_state.temp_email, "token": otp_code, "type": "signup"})
            st.success("¡Cuenta activada! Ya puedes loguearte.")
            st.session_state.view = "login"
            st.rerun()
        except:
            st.error("Código incorrecto o expirado.")

st.markdown('</div>', unsafe_allow_html=True)
