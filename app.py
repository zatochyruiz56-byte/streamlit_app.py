import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth

# CONFIGURACIÓN VISUAL
st.set_page_config(page_title="ZTCHY-PRO", page_icon="🛡️")

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.4), rgba(0,0,0,0.4)), 
                    url('https://images.unsplash.com/photo-1526392060635-9d6019884377?q=80&w=2070');
        background-size: cover;
    }
    .auth-card {
        background-color: white !important;
        padding: 40px;
        border-radius: 20px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.8);
        max-width: 450px;
        margin: auto;
    }
    h2, p, label { color: black !important; font-weight: 700 !important; }
    div.stButton > button { background-color: #6c5ce7 !important; color: white !important; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# INICIALIZAR FIREBASE (Solo una vez)
if not firebase_admin._apps:
    cred = credentials.Certificate(dict(st.secrets["firebase"]))
    firebase_admin.initialize_app(cred)

if "view" not in st.session_state: st.session_state.view = "login"

st.markdown('<div class="auth-card">', unsafe_allow_html=True)

if st.session_state.view == "login":
    st.markdown("<h2>Entrar a ZTCHY</h2>", unsafe_allow_html=True)
    email = st.text_input("Correo")
    password = st.text_input("Contraseña", type="password")
    if st.button("INGRESAR"):
        st.info("Firebase requiere integración con el frontend para Login directo, ¡pero el registro ya es funcional!")
    if st.button("Crear Cuenta"):
        st.session_state.view = "register"
        st.rerun()

elif st.session_state.view == "register":
    st.markdown("<h2>Nueva Cuenta</h2>", unsafe_allow_html=True)
    new_email = st.text_input("Tu mejor Email")
    new_pass = st.text_input("Contraseña (mínimo 6 caracteres)", type="password")
    if st.button("REGISTRARME"):
        try:
            user = auth.create_user(email=new_email, password=new_pass)
            st.success(f"✅ ¡Usuario creado! ID: {user.uid}")
            st.balloons()
        except Exception as e:
            st.error(f"Error: {e}")
    if st.button("Volver"):
        st.session_state.view = "login"
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)
