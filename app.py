import streamlit as st
from supabase import create_client

# 1. Configuración de página y Conexión
st.set_page_config(page_title="ZTCHY-PRO", page_icon="🛡️", layout="centered")

try:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_SECRET_KEY"] # Usamos la Secret Key para permisos totales
    supabase = create_client(url, key)
except:
    st.error("Error en Secrets. Revisa la configuración en Streamlit.")
    st.stop()

# --- DISEÑO ESTILO SEEKER ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.4), rgba(0,0,0,0.4)), 
                    url('https://images.unsplash.com/photo-1526392060635-9d6019884377?q=80&w=2070');
        background-size: cover;
    }
    .auth-card {
        background-color: rgba(255, 255, 255, 0.98);
        padding: 35px;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        color: #333;
    }
    .stButton > button {
        width: 100%;
        background: linear-gradient(90deg, #6c5ce7, #8e44ad);
        color: white;
        border: none;
        height: 3.5em;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

if "view" not in st.session_state: st.session_state.view = "login"

# --- CONTENEDOR DE AUTENTICACIÓN ---
with st.container():
    st.markdown('<div class="auth-card">', unsafe_allow_html=True)
    
    if st.session_state.view == "login":
        st.markdown("<h2 style='text-align:center;'>Iniciar Sesión</h2>", unsafe_allow_html=True)
        email_in = st.text_input("Correo electrónico")
        pass_in = st.text_input("Contraseña", type="password")
        
        if st.button("Ingresar"):
            try:
                supabase.auth.sign_in_with_password({"email": email_in, "password": pass_in})
                st.success("¡Bienvenido!")
            except: st.error("Credenciales incorrectas")
        
        if st.button("👤 ¿No tienes cuenta? Regístrate"):
            st.session_state.view = "register"
            st.rerun()

    elif st.session_state.view == "register":
        st.markdown("<h2 style='text-align:center;'>Crear Cuenta</h2>", unsafe_allow_html=True)
        u_name = st.text_input("Nombre de Usuario")
        u_email = st.text_input("Correo electrónico")
        u_pass = st.text_input("Contraseña", type="password")
        u_conf = st.text_input("Repetir Contraseña", type="password")
        
        if st.button("Completar Registro"):
            if u_pass != u_conf:
                st.error("Las contraseñas no coinciden")
            elif not u_name or not u_email:
                st.warning("Completa todos los campos")
            else:
                try:
                    # 1. Crear el usuario en la sección de Autenticación
                    res = supabase.auth.sign_up({"email": u_email, "password": u_pass})
                    
                    # 2. Guardar el nombre y saldo en nuestra tabla 'perfiles'
                    if res.user:
                        supabase.table("perfiles").insert({
                            "id": res.user.id,
                            "username": u_name,
                            "email": u_email,
                            "saldo": 0.00
                        }).execute()
                        st.success("✅ ¡Registro exitoso! Revisa tu correo.")
                except Exception as e:
                    st.error(f"Error al registrar: {e}")
        
        if st.button("⬅️ Volver al Login"):
            st.session_state.view = "login"
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
