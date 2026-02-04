import streamlit as st
from supabase import create_client

# Configuración inicial
st.set_page_config(page_title="ZTCHY-PRO", page_icon="🛡️", layout="centered")

# Conexión silenciosa
try:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_SECRET_KEY"] 
    supabase = create_client(url, key)
except:
    st.error("Servicio temporalmente no disponible. Inténtelo más tarde.")
    st.stop()

# Estilos (Manteniendo tu estética de Machu Picchu)
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), 
                    url('https://images.unsplash.com/photo-1526392060635-9d6019884377?q=80&w=2070');
        background-size: cover;
    }
    .auth-card {
        background-color: white;
        padding: 40px;
        border-radius: 15px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.4);
    }
    </style>
    """, unsafe_allow_html=True)

if "view" not in st.session_state: st.session_state.view = "login"

with st.container():
    st.markdown('<div class="auth-card">', unsafe_allow_html=True)
    
    if st.session_state.view == "register":
        st.markdown("<h2 style='text-align:center; color:#333;'>Crear Cuenta</h2>", unsafe_allow_html=True)
        u_name = st.text_input("Nombre de Usuario")
        u_email = st.text_input("Correo electrónico")
        u_pass = st.text_input("Contraseña", type="password")
        u_conf = st.text_input("Repetir Contraseña", type="password")
        
        if st.button("Completar Registro"):
            if u_pass != u_conf:
                st.warning("⚠️ Las contraseñas no coinciden.")
            elif not u_name or not u_email:
                st.warning("⚠️ Por favor, completa todos los campos.")
            else:
                # --- BLOQUE DE PROTECCIÓN (Try/Except) ---
                try:
                    res = supabase.auth.sign_up({"email": u_email, "password": u_pass})
                    if res.user:
                        supabase.table("perfiles").insert({
                            "id": res.user.id, "username": u_name, "email": u_email, "saldo": 0.00
                        }).execute()
                        st.session_state.email_temp = u_email
                        st.session_state.view = "verify"
                        st.rerun()
                except Exception as e:
                    # Capturamos el error pero le mostramos algo amigable al cliente
                    error_str = str(e).lower()
                    if "rate limit" in error_str:
                        st.error("🚀 ¡Demasiados intentos! Por seguridad, espera 5 minutos para volver a intentarlo.")
                    elif "already registered" in error_str:
                        st.error("📧 Este correo ya está registrado. Intenta iniciar sesión.")
                    else:
                        st.error("📡 Error de conexión. Por favor, verifica tus datos o intenta más tarde.")
        
        if st.button("⬅️ Volver al Login"):
            st.session_state.view = "login"
            st.rerun()
            
    # (Aquí irían las otras vistas: login y verify, con la misma lógica de mensajes amigables)
    st.markdown('</div>', unsafe_allow_html=True)
