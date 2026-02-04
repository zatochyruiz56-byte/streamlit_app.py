import streamlit as st
from supabase import create_client

# 1. CONFIGURACIÓN DE PÁGINA Y ESTILOS
st.set_page_config(page_title="ZTCHY-PRO", page_icon="🛡️", layout="centered")

# Inyectar CSS para eliminar la línea blanca superior, fondo y tarjetas
st.markdown("""
    <style>
    /* Eliminar línea blanca superior y menús innecesarios */
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stAppDeployButton {display:none;}
    
    /* Fondo de Machu Picchu con overlay oscuro para contraste */
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), 
                    url('https://images.unsplash.com/photo-1526392060635-9d6019884377?q=80&w=2070');
        background-size: cover;
        background-position: center;
    }

    /* Tarjetas Blancas (Auth Cards) */
    .auth-card {
        background-color: rgba(255, 255, 255, 0.95);
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.3);
        color: #1e1e1e; /* Letras oscuras para visibilidad */
        margin-top: 20px;
    }

    /* Estilo de los Inputs y Textos */
    .stTextInput label {
        color: #1e1e1e !important;
        font-weight: bold;
    }
    
    h2, h3, p {
        color: #1e1e1e !important;
        text-align: center;
    }

    /* Botones estilo Púrpura */
    .stButton > button {
        width: 100%;
        background: #6c5ce7;
        color: white !important;
        font-weight: bold;
        border-radius: 8px;
        border: none;
        height: 3em;
        transition: 0.3s;
    }
    .stButton > button:hover {
        background: #5b4bc4;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. CONEXIÓN A SUPABASE
try:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_SECRET_KEY"] 
    supabase = create_client(url, key)
except:
    st.error("Error de configuración: Revisa tus Secrets en Streamlit.")
    st.stop()

# 3. LÓGICA DE ESTADO
if "view" not in st.session_state: st.session_state.view = "login"
if "user" not in st.session_state: st.session_state.user = None
if "email_temp" not in st.session_state: st.session_state.email_temp = ""

# 4. INTERFAZ DE USUARIO
with st.container():
    st.markdown('<div class="auth-card">', unsafe_allow_html=True)
    
    # LOGO
    st.markdown("<h1 style='text-align:center; color:#6c5ce7;'>🛡️ ZTCHY-PRO</h1>", unsafe_allow_html=True)

    # --- VISTA: LOGIN ---
    if st.session_state.view == "login":
        st.markdown("<h2>Iniciar Sesión</h2>", unsafe_allow_html=True)
        email = st.text_input("Correo Electrónico", key="l_email")
        password = st.text_input("Contraseña", type="password", key="l_pass")
        
        if st.button("Ingresar"):
            try:
                res = supabase.auth.sign_in_with_password({"email": email, "password": password})
                if res.user:
                    p = supabase.table("perfiles").select("*").eq("id", res.user.id).single().execute()
                    st.session_state.user = p.data
                    st.rerun()
            except: st.error("Credenciales incorrectas o cuenta no verificada.")
        
        st.markdown("<p>¿No tienes cuenta?</p>", unsafe_allow_html=True)
        if st.button("Crear Cuenta Nueva"):
            st.session_state.view = "register"
            st.rerun()

    # --- VISTA: REGISTRO ---
    elif st.session_state.view == "register":
        st.markdown("<h2>Crear Cuenta</h2>", unsafe_allow_html=True)
        u_name = st.text_input("Nombre de Usuario")
        u_email = st.text_input("Correo Electrónico")
        u_pass = st.text_input("Contraseña", type="password")
        
        if st.button("Registrar Ahora"):
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
        
        if st.button("⬅ Volver al Login"):
            st.session_state.view = "login"
            st.rerun()

    # --- VISTA: VERIFICACIÓN (CÓDIGO OTP) ---
    elif st.session_state.view == "verify":
        st.markdown("<h2>Verifica tu Email</h2>", unsafe_allow_html=True)
        st.markdown(f"<p>Ingresa el código enviado a:<br><b>{st.session_state.email_temp}</b></p>", unsafe_allow_html=True)
        
        otp_code = st.text_input("Código de 6 dígitos", max_chars=6)
        
        if st.button("Validar Cuenta"):
            try:
                supabase.auth.verify_otp({
                    "email": st.session_state.email_temp, 
                    "token": otp_code, 
                    "type": 'signup'
                })
                st.success("¡Cuenta activada! Ya puedes loguearte.")
                st.session_state.view = "login"
                st.rerun()
            except:
                st.error("Código incorrecto o expirado.")
        
        if st.button("⬅ Reintentar Registro"):
            st.session_state.view = "register"
            st.rerun()

    # --- VISTA: PANEL PRINCIPAL ---
    elif st.session_state.view == "main" or st.session_state.user:
        st.markdown(f"<h2>Bienvenido, {st.session_state.user['username']}</h2>", unsafe_allow_html=True)
        st.metric(label="Saldo Disponible", value=f"${st.session_state.user['saldo']:.2f}")
        
        if st.button("Cerrar Sesión"):
            supabase.auth.sign_out()
            st.session_state.user = None
            st.session_state.view = "login"
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
