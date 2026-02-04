import streamlit as st
from supabase import create_client

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="ZTCHY-PRO", page_icon="🛡️", layout="centered")

# 2. DISEÑO CSS PERSONALIZADO (Tarjetas blancas y texto oscuro)
st.markdown("""
    <style>
    /* Ocultar elementos nativos de Streamlit para limpieza total */
    header, footer, .stAppDeployButton, #MainMenu {visibility: hidden;}
    [data-testid="stSidebar"] {display: none;}
    
    /* Fondo de Machu Picchu con capa de contraste */
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.3), rgba(0,0,0,0.3)), 
                    url('https://images.unsplash.com/photo-1526392060635-9d6019884377?q=80&w=2070');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    /* Estilo de la Tarjeta Blanca (Auth Card) */
    .auth-card {
        background-color: #ffffff;
        padding: 40px;
        border-radius: 25px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.5);
        max-width: 450px;
        margin: auto;
    }

    /* Forzar visibilidad de textos (Negro/Gris Oscuro) */
    h2, p, label, .stMarkdown {
        color: #2d3436 !important;
        font-family: 'Helvetica Neue', Arial, sans-serif;
    }
    
    h2 { text-align: left; font-weight: 800; font-size: 32px; margin-bottom: 10px; }
    p { font-size: 15px; margin-bottom: 20px; }

    /* Botones Púrpuras Modernos */
    div.stButton > button {
        background-color: #6c5ce7 !important;
        color: white !important;
        border-radius: 12px !important;
        border: none !important;
        width: 100%;
        height: 50px;
        font-weight: bold;
        font-size: 16px;
        margin-top: 15px;
        transition: 0.3s;
    }
    
    div.stButton > button:hover {
        background-color: #5b4bc4 !important;
        transform: translateY(-2px);
    }

    /* Inputs de texto limpios */
    .stTextInput input {
        border-radius: 10px !important;
        border: 1px solid #dfe6e9 !important;
        padding: 12px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. CONEXIÓN A SUPABASE (Asegúrate de tener tus Secrets configurados)
try:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_SECRET_KEY"]
    supabase = create_client(url, key)
except:
    st.error("Error: Configura SUPABASE_URL y SUPABASE_SECRET_KEY en los Secrets de Streamlit.")
    st.stop()

# 4. MANEJO DE NAVEGACIÓN
if "view" not in st.session_state: st.session_state.view = "login"
if "user" not in st.session_state: st.session_state.user = None
if "email_temp" not in st.session_state: st.session_state.email_temp = ""

# LOGO SUPERIOR (Centrado)
st.image("https://i.ibb.co/L9Y0Y5T/Logo-Z.png", width=100) # Sustituir por el enlace directo a tu logo blanco de la "Z"

# INICIO DE TARJETA BLANCA
st.markdown('<div class="auth-card">', unsafe_allow_html=True)

# --- PANTALLA: LOGIN ---
if st.session_state.view == "login":
    st.markdown("<h2>Iniciar Sesión</h2>", unsafe_allow_html=True)
    st.markdown("<p>Ingresa a tu cuenta segura de ZTCHY-PRO</p>", unsafe_allow_html=True)
    
    l_email = st.text_input("Correo electrónico")
    l_pass = st.text_input("Contraseña", type="password")
    
    if st.button("Ingresar"):
        try:
            res = supabase.auth.sign_in_with_password({"email": l_email, "password": l_pass})
            if res.user:
                p = supabase.table("perfiles").select("*").eq("id", res.user.id).single().execute()
                st.session_state.user = p.data
                st.rerun()
        except:
            st.error("Credenciales incorrectas o cuenta no activada.")
    
    if st.button("Crear Cuenta Nueva", key="goto_reg"):
        st.session_state.view = "register"
        st.rerun()

# --- PANTALLA: REGISTRO ---
elif st.session_state.view == "register":
    st.markdown("<h2>Crear Cuenta</h2>", unsafe_allow_html=True)
    st.markdown("<p>Regístrate para comenzar a operar</p>", unsafe_allow_html=True)
    
    u_name = st.text_input("Nombre de Usuario")
    u_email = st.text_input("Correo Electrónico")
    u_pass = st.text_input("Contraseña", type="password")
    
    if st.button("Completar Registro"):
        try:
            # Registro en Auth
            res = supabase.auth.sign_up({"email": u_email, "password": u_pass})
            if res.user:
                # Insertar en tabla perfiles
                supabase.table("perfiles").insert({
                    "id": res.user.id, "username": u_name, "email": u_email, "saldo": 0.0
                }).execute()
                st.session_state.email_temp = u_email
                st.session_state.view = "verify"
                st.rerun()
        except Exception as e:
            st.error(f"Error al registrar: {e}")
            
    if st.button("Volver al Login"):
        st.session_state.view = "login"
        st.rerun()

# --- PANTALLA: VERIFICACIÓN (OTP) ---
elif st.session_state.view == "verify":
    st.markdown("<h2>Verifica tu Correo</h2>", unsafe_allow_html=True)
    st.markdown(f"<p>Hemos enviado un código a:<br><b>{st.session_state.email_temp}</b></p>", unsafe_allow_html=True)
    
    otp_code = st.text_input("Código de 6 dígitos", max_chars=6)
    
    if st.button("Validar Cuenta"):
        try:
            supabase.auth.verify_otp({
                "email": st.session_state.email_temp, 
                "token": otp_code, 
                "type": 'signup'
            })
            st.success("¡Cuenta activada con éxito!")
            st.session_state.view = "login"
            st.rerun()
        except:
            st.error("Código incorrecto o expirado.")

# CIERRE DE TARJETA BLANCA
st.markdown('</div>', unsafe_allow_html=True)

# --- PANEL PRINCIPAL (Fuera de la tarjeta si quieres más espacio) ---
if st.session_state.user:
    st.markdown(f"<h2 style='color:white;'>Bienvenido, {st.session_state.user['username']}</h2>", unsafe_allow_html=True)
    st.metric("Saldo Disponible", f"${st.session_state.user['saldo']:.2f}")
    if st.button("Cerrar Sesión"):
        supabase.auth.sign_out()
        st.session_state.user = None
        st.session_state.view = "login"
        st.rerun()
