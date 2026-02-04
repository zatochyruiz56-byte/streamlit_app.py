import streamlit as st
from supabase import create_client

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="ZTCHY-PRO", page_icon="🛡️", layout="centered")

# 2. ESTILOS CSS PERSONALIZADOS (Diseño de tarjetas blancas y letras visibles)
st.markdown("""
    <style>
    /* Ocultar elementos nativos de Streamlit */
    header, footer, .stAppDeployButton, #MainMenu {visibility: hidden;}
    
    /* Fondo de Machu Picchu fijo */
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.4), rgba(0,0,0,0.4)), 
                    url('https://images.unsplash.com/photo-1526392060635-9d6019884377?q=80&w=2070');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    /* Contenedor de la Tarjeta Blanca */
    .auth-card {
        background-color: #f8f9fa;
        padding: 40px;
        border-radius: 10px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.5);
        margin: auto;
        max-width: 450px;
    }

    /* Forzar visibilidad de textos (Negro/Gris Oscuro) */
    .stMarkdown, p, h2, h3, label {
        color: #1f1f1f !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    h2 { text-align: center; font-weight: 700; margin-bottom: 20px; }

    /* Botones Púrpuras */
    div.stButton > button {
        background-color: #6c5ce7 !important;
        color: white !important;
        border-radius: 5px !important;
        border: none !important;
        width: 100%;
        height: 45px;
        font-weight: bold;
        text-transform: uppercase;
        margin-top: 10px;
    }
    
    div.stButton > button:hover {
        background-color: #5b4bc4 !important;
        border: none !important;
    }

    /* Inputs con bordes sutiles */
    .stTextInput input {
        border-radius: 5px !important;
        border: 1px solid #ddd !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. CONEXIÓN A SUPABASE
try:
    supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_SECRET_KEY"])
except:
    st.error("Error: Configura los Secrets en Streamlit.")
    st.stop()

# 4. MANEJO DE ESTADOS (Para mostrar una pantalla a la vez)
if "view" not in st.session_state: st.session_state.view = "login"
if "user" not in st.session_state: st.session_state.user = None
if "email_temp" not in st.session_state: st.session_state.email_temp = ""

# --- LÓGICA DE INTERFAZ ---

# Contenedor principal para centrar el logo y la tarjeta
st.image("https://i.imgur.com/vHqY7Z8.png", width=80) # Aquí puedes subir tu logo 'Z' a un host y poner el link
st.markdown("<h1 style='text-align:center; color:white; margin-bottom:20px;'>ZTCHY-PRO</h1>", unsafe_allow_html=True)

# Inicio de Tarjeta Blanca
st.markdown('<div class="auth-card">', unsafe_allow_html=True)

# --- PANTALLA 1: LOGIN ---
if st.session_state.view == "login" and not st.session_state.user:
    st.markdown("<h2>Iniciar Sesión</h2>", unsafe_allow_html=True)
    l_email = st.text_input("Correo electrónico")
    l_pass = st.text_input("Contraseña", type="password")
    
    if st.button("Ingresar"):
        try:
            res = supabase.auth.sign_in_with_password({"email": l_email, "password": l_pass})
            if res.user:
                p = supabase.table("perfiles").select("*").eq("id", res.user.id).single().execute()
                st.session_state.user = p.data
                st.rerun()
        except: st.error("Error: Verifica tus datos o activa tu cuenta.")
    
    if st.button("¿No tienes cuenta? Regístrate"):
        st.session_state.view = "register"
        st.rerun()

# --- PANTALLA 2: REGISTRO ---
elif st.session_state.view == "register":
    st.markdown("<h2>Crear Cuenta</h2>", unsafe_allow_html=True)
    u_name = st.text_input("Nombre de Usuario")
    u_email = st.text_input("Correo Electrónico")
    u_pass = st.text_input("Contraseña", type="password")
    
    if st.button("Completar Registro"):
        try:
            res = supabase.auth.sign_up({"email": u_email, "password": u_pass})
            if res.user:
                supabase.table("perfiles").insert({
                    "id": res.user.id, "username": u_name, "email": u_email, "saldo": 0.0
                }).execute()
                st.session_state.email_temp = u_email
                st.session_state.view = "verify"
                st.rerun()
        except Exception as e:
            st.error(f"Error: {e}")
            
    if st.button("Volver al Login"):
        st.session_state.view = "login"
        st.rerun()

# --- PANTALLA 3: VERIFICACIÓN ---
elif st.session_state.view == "verify":
    st.markdown("<h2>Verifica tu Correo</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center;'>Ingresa el código enviado a:<br><b>{st.session_state.email_temp}</b></p>", unsafe_allow_html=True)
    
    otp = st.text_input("Código de 6 dígitos", max_chars=6)
    
    if st.button("Validar Cuenta"):
        try:
            supabase.auth.verify_otp({"email": st.session_state.email_temp, "token": otp, "type": 'signup'})
            st.success("¡Cuenta activada!")
            st.session_state.view = "login"
            st.rerun()
        except:
            st.error("Código incorrecto.")
            
    if st.button("Cancelar"):
        st.session_state.view = "login"
        st.rerun()

# --- PANTALLA 4: PANEL PRINCIPAL (Dashboard) ---
elif st.session_state.user:
    st.markdown(f"<h2>Bienvenido, {st.session_state.user['username']}</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>Tu panel de control seguro.</p>", unsafe_allow_html=True)
    
    st.metric(label="Saldo en Cuenta", value=f"${st.session_state.user['saldo']:.2f}")
    
    if st.button("Cerrar Sesión"):
        supabase.auth.sign_out()
        st.session_state.user = None
        st.session_state.view = "login"
        st.rerun()

# Cierre de Tarjeta Blanca
st.markdown('</div>', unsafe_allow_html=True)
