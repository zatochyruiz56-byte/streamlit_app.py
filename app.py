import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth, firestore
import requests
import random

# --- 1. EL MURO (CONFIGURACIÓN VISUAL) ---
st.set_page_config(page_title="ZTCHY PRO", layout="centered")

# Fondo de Machu Picchu que bloquea todo
st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), 
                    url("https://images.unsplash.com/photo-1526392060635-9d6019884377?q=80&w=2070&auto=format&fit=crop");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    /* Ocultar barra lateral si no hay login */
    [data-testid="stSidebar"] {{
        display: {"block" if st.session_state.get('auth_active', False) else "none"};
    }}
    .auth-container {{
        background-color: rgba(255, 255, 255, 0.95);
        padding: 30px;
        border-radius: 15px;
        color: black;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. INICIALIZACIÓN DE CEREBRO (FIREBASE) ---
if not firebase_admin._apps:
    fb_dict = dict(st.secrets["firebase"])
    fb_dict["private_key"] = fb_dict["private_key"].replace('\\n', '\n')
    cred = credentials.Certificate(fb_dict)
    firebase_admin.initialize_app(cred)

db = firestore.client()

# --- 3. ESTADO DEL CEREBRO ---
if "auth_active" not in st.session_state:
    st.session_state.auth_active = False
if "user_data" not in st.session_state:
    st.session_state.user_data = None
if "step" not in st.session_state:
    st.session_state.step = "login"

# --- 4. FUNCIONES DEL SISTEMA ---
def send_otp(email, code):
    url = "https://api.mailersend.com/v1/email"
    headers = {"Authorization": f"Bearer {st.secrets['mailersend_api_key']}", "Content-Type": "application/json"}
    payload = {
        "from": {"email": f"MS_ALHbS4@{st.secrets['mailersend_domain']}"}, # Dominio verificado
        "to": [{"email": email}],
        "subject": "Código de Verificación ZTCHY",
        "html": f"<h2>Tu código es: {code}</h2>"
    }
    return requests.post(url, json=payload, headers=headers)

# --- 5. LÓGICA DE CAPAS (EL FILTRO) ---

# CAPA A: ACCESO RESTRINGIDO (LOGIN/REGISTRO)
if not st.session_state.auth_active:
    st.markdown('<div class="auth-container">', unsafe_allow_html=True)
    
    if st.session_state.step == "login":
        st.title("🏔️ ZTCHY PRO")
        email_log = st.text_input("Correo")
        pass_log = st.text_input("Contraseña", type="password")
        
        if st.button("Iniciar Sesión", use_container_width=True):
            try:
                user = auth.get_user_by_email(email_log)
                st.session_state.user_data = {"uid": user.uid, "email": user.email}
                st.session_state.auth_active = True
                st.rerun()
            except:
                st.error("Credenciales incorrectas o usuario no registrado.")
        
        if st.button("No tengo cuenta", use_container_width=True):
            st.session_state.step = "register"
            st.rerun()

    elif st.session_state.step == "register":
        st.title("📝 Registro Nuevo")
        reg_email = st.text_input("Correo nuevo")
        reg_pass = st.text_input("Clave nueva", type="password")
        
        if st.button("Enviar Código", use_container_width=True):
            if reg_email and reg_pass:
                st.session_state.temp_otp = str(random.randint(100000, 999999))
                st.session_state.temp_user = {"email": reg_email, "pass": reg_pass}
                send_otp(reg_email, st.session_state.temp_otp)
                st.session_state.step = "verify"
                st.rerun()

    elif st.session_state.step == "verify":
        st.title("🛡️ Verifica tu correo")
        otp_in = st.text_input("Código de 6 dígitos")
        if st.button("Validar y Entrar"):
            if otp_in == st.session_state.temp_otp:
                user = auth.create_user(
                    email=st.session_state.temp_user["email"],
                    password=st.session_state.temp_user["pass"]
                )
                # Crear saldo inicial en Firestore
                db.collection("usuarios").document(user.uid).set({"email": user.email, "saldo": 10})
                st.success("¡Cuenta creada! Inicia sesión.")
                st.session_state.step = "login"
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# CAPA B: PANEL DE CONTROL (SÓLO SI AUTH_ACTIVE ES TRUE)
else:
    # Aquí el cerebro ya sabe que user_data existe, no habrá AttributeError
    u_info = st.session_state.user_data
    
    # Menú Lateral
    st.sidebar.title("Panel ZTCHY")
    st.sidebar.write(f"Usuario: {u_info['email']}")
    
    # Obtener saldo de Firestore
    doc = db.collection("usuarios").document(u_info['uid']).get()
    saldo = doc.to_dict().get("saldo", 0) if doc.exists else 0
    
    st.sidebar.metric("Saldo Disponible", f"{saldo} créditos")
    
    if st.sidebar.button("Cerrar Sesión"):
        st.session_state.auth_active = False
        st.rerun()

    # Contenido Principal
    st.title("🔍 Sistema de Consultas")
    query = st.text_input("¿Qué deseas consultar hoy?")
    
    if st.button("Realizar Consulta (-1 crédito)"):
        if saldo > 0:
            with st.spinner("Procesando..."):
                # Restar saldo en Firestore
                db.collection("usuarios").document(u_info['uid']).update({"saldo": firestore.Increment(-1)})
                st.success("Consulta exitosa. Se ha descontado 1 crédito.")
                st.rerun()
        else:
            st.error("⚠️ Saldo insuficiente.")
