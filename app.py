import streamlit as st
from supabase import create_client

# 1. Configuración de página y Conexión
st.set_page_config(page_title="ZTCHY-PRO", page_icon="🛡️", layout="centered")

try:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase = create_client(url, key)
except:
    st.error("Error en Secrets")
    st.stop()

# Estilos CSS para imitar la interfaz de "Seeker"
st.markdown("""
    <style>
    .main { background: linear-gradient(to bottom, #2c3e50, #4ca1af); }
    .auth-card {
        background-color: white;
        padding: 40px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        color: #333;
    }
    div.stButton > button {
        width: 100%;
        border-radius: 8px;
        height: 3em;
        background-color: #6c5ce7;
        color: white;
        font-weight: bold;
        border: none;
    }
    div.stButton > button:hover { background-color: #a29bfe; color: white; }
    </style>
    """, unsafe_allow_html=True)

# Lógica de navegación interna
if "view" not in st.session_state:
    st.session_state.view = "login"

# --- VISTA: INICIAR SESIÓN ---
if st.session_state.view == "login":
    st.markdown("<h2 style='text-align: center;'>Iniciar Sesión</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>ZTCHY-PRO v2 - 2026</p>", unsafe_allow_html=True)
    
    with st.container():
        email = st.text_input("Nombre de Usuario | Correo")
        password = st.text_input("Contraseña", type="password")
        
        if st.button("Ingresar"):
            try:
                res = supabase.auth.sign_in_with_password({"email": email, "password": password})
                st.success("¡Bienvenido!")
                st.session_state.user = res.user
            except:
                st.error("Credenciales incorrectas")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("➕ Registrarse"):
                st.session_state.view = "register"
                st.rerun()
        with col2:
            if st.button("❓ ¿Olvidaste tu contraseña?"):
                st.session_state.view = "forgot"
                st.rerun()

# --- VISTA: REGISTRARSE ---
elif st.session_state.view == "register":
    st.markdown("<h2 style='text-align: center;'>Registrarse</h2>", unsafe_allow_html=True)
    
    user_reg = st.text_input("Username / Nombre de Usuario")
    email_reg = st.text_input("Correo electrónico")
    pass_reg = st.text_input("Contraseña", type="password")
    pass_conf = st.text_input("Repetir Contraseña", type="password")
    
    if st.button("Registrar"):
        if pass_reg != pass_conf:
            st.error("Las contraseñas no coinciden")
        elif user_reg and email_reg:
            try:
                auth_res = supabase.auth.sign_up({"email": email_reg, "password": pass_reg})
                supabase.table("perfiles").insert({"id": auth_res.user.id, "username": user_reg, "email": email_reg}).execute()
                st.success("Registro iniciado. ¡Revisa tu correo para el código!")
                st.session_state.email_temporal = email_reg
                st.session_state.view = "verify"
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")
                
    if st.button("Ya tengo cuenta, Iniciar Sesión"):
        st.session_state.view = "login"
        st.rerun()

# --- VISTA: RECUPERAR CONTRASEÑA ---
elif st.session_state.view == "forgot":
    st.markdown("<h3 style='text-align: center;'>¿Olvidaste tu contraseña?</h3>", unsafe_allow_html=True)
    st.write("Ingresa tu correo para resetear tu contraseña.")
    email_reset = st.text_input("Correo Electrónico")
    
    if st.button("Enviar correo electrónico"):
        try:
            supabase.auth.reset_password_for_email(email_reset)
            st.success("Si el correo existe, recibirás un enlace de recuperación.")
        except:
            st.error("Error al procesar la solicitud")
            
    if st.button("Regresar"):
        st.session_state.view = "login"
        st.rerun()

# --- VISTA: VERIFICACIÓN OTP (EL CÓDIGO) ---
elif st.session_state.view == "verify":
    st.markdown("<h2 style='text-align: center;'>Verificar Cuenta</h2>", unsafe_allow_html=True)
    st.info(f"Ingresa el código enviado a {st.session_state.email_temporal}")
    otp_code = st.text_input("Código de 8 dígitos")
    
    if st.button("Confirmar y Activar"):
        try:
            supabase.auth.verify_otp({"email": st.session_state.email_temporal, "token": otp_code, "type": 'signup'})
            st.success("¡Cuenta activada! Ya puedes iniciar sesión.")
            st.session_state.view = "login"
            st.rerun()
        except:
            st.error("Código incorrecto")
