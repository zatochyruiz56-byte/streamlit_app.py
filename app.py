import streamlit as st
from supabase import create_client

# Configuración premium
st.set_page_config(page_title="ZTCHY-PRO", page_icon="🛡️", layout="centered")

# Conexión
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_SECRET_KEY"] 
supabase = create_client(url, key)

# Estilos CSS (Fondo Machu Picchu)
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.4), rgba(0,0,0,0.4)), 
                    url('https://images.unsplash.com/photo-1526392060635-9d6019884377?q=80&w=2070');
        background-size: cover;
    }
    .auth-card {
        background-color: rgba(255, 255, 255, 0.98);
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    </style>
    """, unsafe_allow_html=True)

if "view" not in st.session_state: st.session_state.view = "login"

with st.container():
    st.markdown('<div class="auth-card">', unsafe_allow_html=True)
    
    if st.session_state.view == "login":
        st.markdown("<h2 style='text-align:center; color:#333;'>Iniciar Sesión</h2>", unsafe_allow_html=True)
        email = st.text_input("Correo electrónico")
        pw = st.text_input("Contraseña", type="password")
        if st.button("Ingresar"):
            try:
                supabase.auth.sign_in_with_password({"email": email, "password": pw})
                st.success("¡Bienvenido!")
            except: st.error("Error al entrar")
        if st.button("👤 Crear Cuenta"):
            st.session_state.view = "register"
            st.rerun()

    elif st.session_state.view == "register":
        st.markdown("<h2 style='text-align:center; color:#333;'>Registrarse</h2>", unsafe_allow_html=True)
        u_name = st.text_input("Nombre de Usuario")
        u_email = st.text_input("Correo electrónico")
        u_pass = st.text_input("Contraseña", type="password")
        u_conf = st.text_input("Repetir Contraseña", type="password")
        
        if st.button("Registrar"):
            if u_pass != u_conf: st.error("Las contraseñas no coinciden")
            else:
                try:
                    # 1. Registrar en Auth
                    res = supabase.auth.sign_up({"email": u_email, "password": u_pass})
                    # 2. Insertar en tabla perfiles usando el ID generado
                    supabase.table("perfiles").insert({
                        "id": res.user.id,
                        "username": u_name,
                        "email": u_email,
                        "saldo": 0.0
                    }).execute()
                    st.success("¡Revisa tu correo para confirmar!")
                except Exception as e: st.error(f"Error: {e}")
        
        if st.button("Volver"):
            st.session_state.view = "login"
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
