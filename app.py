import streamlit as st
from supabase import create_client

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="ZTCHY-PRO", page_icon="🛡️", layout="centered")

# 2. DISEÑO CSS PROFESIONAL (Copiando el estilo de las tarjetas blancas)
st.markdown("""
    <style>
    /* Ocultar elementos de Streamlit */
    header, footer, .stAppDeployButton, #MainMenu {visibility: hidden;}
    [data-testid="stSidebar"] {display: none;}
    
    /* Fondo Machu Picchu */
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.2), rgba(0,0,0,0.2)), 
                    url('https://images.unsplash.com/photo-1526392060635-9d6019884377?q=80&w=2070');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    /* Estilo de la Tarjeta Blanca (Auth Card) */
    .auth-card {
        background-color: #fcfcfc;
        padding: 40px;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.4);
        max-width: 450px;
        margin: auto;
        border: 1px solid #eeeeee;
    }

    /* Textos y Etiquetas */
    h2 {
        color: #2d3436 !important;
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 700;
        text-align: left;
        margin-bottom: 5px;
        font-size: 28px;
    }
    
    .stMarkdown p, label {
        color: #636e72 !important;
        font-weight: 500 !important;
        font-size: 14px !important;
    }

    /* Inputs Limpios */
    .stTextInput input {
        background-color: #ffffff !important;
        border: 1px solid #dfe6e9 !important;
        border-radius: 8px !important;
        padding: 10px !important;
        color: #2d3436 !important;
    }

    /* Botones Púrpuras Estilo Moderno */
    div.stButton > button {
        background-color: #6c5ce7 !important;
        color: white !important;
        border-radius: 10px !important;
        border: none !important;
        width: 100%;
        height: 50px;
        font-weight: bold;
        font-size: 16px;
        transition: 0.3s;
        box-shadow: 0 4px 15px rgba(108, 92, 231, 0.3);
    }
    
    div.stButton > button:hover {
        background-color: #5b4bc4 !important;
        transform: translateY(-2px);
    }

    /* Link de volver / Registrarse */
    .stButton button[kind="secondary"] {
        background: transparent !important;
        color: #6c5ce7 !important;
        box-shadow: none !important;
        font-size: 14px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. CONEXIÓN (Secrets)
supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_SECRET_KEY"])

# 4. LÓGICA DE NAVEGACIÓN
if "view" not in st.session_state: st.session_state.view = "login"
if "user" not in st.session_state: st.session_state.user = None

# Logo centrado arriba de la tarjeta
col1, col2, col3 = st.columns([1,1,1])
with col2:
    st.image("https://i.ibb.co/L9Y0Y5T/Logo-Z.png", width=100) # Reemplazar con URL de tu logo Z

st.markdown('<div class="auth-card">', unsafe_allow_html=True)

# --- PANTALLA: LOGIN ---
if st.session_state.view == "login" and not st.session_state.user:
    st.markdown("<h2>Iniciar Sesión</h2>", unsafe_allow_html=True)
    email = st.text_input("Correo electrónico")
    password = st.text_input("Contraseña", type="password")
    
    if st.button("Ingresar"):
        try:
            res = supabase.auth.sign_in_with_password({"email": email, "password": password})
            if res.user:
                p = supabase.table("perfiles").select("*").eq("id", res.user.id).single().execute()
                st.session_state.user = p.data
                st.rerun()
        except: st.error("Error en credenciales")
    
    if st.button("¿No tienes cuenta? Regístrate", key="btn_reg"):
        st.session_state.view = "register"
        st.rerun()

# --- PANTALLA: REGISTRO ---
elif st.session_state.view == "register":
    st.markdown("<h2>Crear Cuenta</h2>", unsafe_allow_html=True)
    name = st.text_input("Nombre de Usuario")
    mail = st.text_input("Correo Electrónico")
    pw = st.text_input("Contraseña", type="password")
    
    if st.button("Completar Registro"):
        try:
            res = supabase.auth.sign_up({"email": mail, "password": pw})
            if res.user:
                supabase.table("perfiles").insert({"id": res.user.id, "username": name, "email": mail, "saldo": 0.0}).execute()
                st.session_state.email_temp = mail
                st.session_state.view = "verify"
                st.rerun()
        except Exception as e: st.error(f"Error: {e}")
            
    if st.button("Volver al Login"):
        st.session_state.view = "login"
        st.rerun()

# --- PANTALLA: VERIFICACIÓN ---
elif st.session_state.view == "verify":
    st.markdown("<h2>Verifica tu Correo</h2>", unsafe_allow_html=True)
    st.write(f"Ingresa el código enviado a: **{st.session_state.email_temp}**")
    otp = st.text_input("Código de 6 dígitos")
    
    if st.button("Validar y Activar"):
        try:
            supabase.auth.verify_otp({"email": st.session_state.email_temp, "token": otp, "type": 'signup'})
            st.success("¡Activado!")
            st.session_state.view = "login"
            st.rerun()
        except: st.error("Código incorrecto")

# --- PANTALLA: DASHBOARD (Al loguearse) ---
elif st.session_state.user:
    st.markdown(f"<h2>Hola, {st.session_state.user['username']}</h2>", unsafe_allow_html=True)
    st.metric("Tu Saldo Actual", f"${st.session_state.user['saldo']}")
    if st.button("Cerrar Sesión"):
        supabase.auth.sign_out()
        st.session_state.user = None
        st.session_state.view = "login"
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)
