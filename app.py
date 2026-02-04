import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth, firestore
import requests
import random

# --- 1. CONFIGURACIÓN E INYECCIÓN VISUAL ---
st.set_page_config(page_title="ZTCHY PRO", layout="centered")

# Fondo de Machu Picchu y ocultamiento total de la barra lateral si no hay login
st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.65), rgba(0,0,0,0.65)), 
                    url("https://images.unsplash.com/photo-1526392060635-9d6019884377?q=80&w=2070&auto=format&fit=crop");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    [data-testid="stSidebar"] {{
        display: {"block" if st.session_state.get('authenticated', False) else "none"};
    }}
    .auth-card {{
        background-color: rgba(255, 255, 255, 0.98);
        padding: 2.5rem;
        border-radius: 20px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.5);
        color: #121212;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. INICIALIZACIÓN DE SERVICIOS ---
if not firebase_admin._apps:
    fb_dict = dict(st.secrets["firebase"])
    fb_dict["private_key"] = fb_dict["private_key"].replace('\\n', '\n')
    cred = credentials.Certificate(fb_dict)
    firebase_admin.initialize_app(cred)

db = firestore.client()

# --- 3. FUNCIONES DE APOYO ---
def send_otp(email, code):
    url = "https://api.mailersend.com/v1/email"
    headers = {
        "Authorization": f"Bearer {st.secrets['mailersend_api_key']}", # Usando token verificado
        "Content-Type": "application/json"
    }
    payload = {
        "from": {"email": f"MS_ALHbS4@{st.secrets['mailersend_domain']}"},
        "to": [{"email": email}],
        "subject": "Código de Acceso ZTCHY",
        "html": f"<div style='text-align:center;'><h1>Código: {code}</h1></div>"
    }
    return requests.post(url, json=payload, headers=headers)

# --- 4. GESTIÓN DE SESIÓN ---
# Inicializamos todas las llaves para evitar el AttributeError
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_data" not in st.session_state:
    st.session_state.user_data = None
if "view" not in st.session_state:
    st.session_state.view = "login"

# --- 5. INTERFAZ: MURO DE ACCESO ---
if not st.session_state.authenticated:
    st.markdown('<div class="auth-card">', unsafe_allow_html=True)
    
    if st.session_state.view == "login":
        st.title("🏔️ ZTCHY PRO")
        st.caption("Ingresa para acceder al sistema")
        login_email = st.text_input("Correo electrónico", key="log_e")
        login_pass = st.text_input("Contraseña", type="password", key="log_p")
        
        if st.button("Entrar", use_container_width=True):
            try:
                user = auth.get_user_by_email(login_email)
                # Seteamos los datos antes de cambiar el estado de autenticación
                st.session_state.user_data = {"uid": user.uid, "email": user.email}
                st.session_state.authenticated = True
                st.rerun()
            except:
                st.error("Credenciales incorrectas o cuenta no registrada.")
        
        st.divider()
        if st.button("Crear cuenta nueva", use_container_width=True):
            st.session_state.view = "register"
            st.rerun()

    elif st.session_state.view == "register":
        st.title("📝 Nuevo Registro")
        reg_email = st.text_input("Tu correo")
        reg_pass = st.text_input("Crea una contraseña", type="password")
        
        if st.button("Enviar Código OTP", use_container_width=True):
            if reg_email and len(reg_pass) >= 6:
                st.session_state.generated_code = str(random.randint(100000, 999999))
                st.session_state.pending_user = {"email": reg_email, "pass": reg_pass}
                send_otp(reg_email, st.session_state.generated_code)
                st.session_state.view = "verify"
                st.rerun()
            else:
                st.warning("El correo es obligatorio y la clave debe tener 6+ caracteres.")
        
        if st.button("Volver al inicio"):
            st.session_state.view = "login"
            st.rerun()

    elif st.session_state.view == "verify":
        st.title("🛡️ Verificación")
        code_in = st.text_input("Código enviado")
        if st.button("Confirmar y Crear Cuenta", use_container_width=True):
            if code_in == st.session_state.get('generated_code'):
                # Crear usuario en Firebase Auth
                user = auth.create_user(
                    email=st.session_state.pending_user["email"],
                    password=st.session_state.pending_user["pass"]
                )
                # Crear registro de saldo en Firestore
                db.collection("usuarios").document(user.uid).set({
                    "email": user.email,
                    "saldo": 10
                })
                st.success("¡Cuenta lista! Ya puedes iniciar sesión.")
                st.session_state.view = "login"
                st.rerun()
            else:
                st.error("Código inválido.")
    
    st.markdown('</div>', unsafe_allow_html=True)

# --- 6. INTERFAZ: PANEL EXCLUSIVO (Solo si está autenticado) ---
else:
    # Verificación de seguridad para el sidebar
    user_info = st.session_state.get("user_data")
    
    st.sidebar.title("Panel ZTCHY")
    st.sidebar.write(f"👤 **{user_info['email'] if user_info else 'Usuario'}**")
    
    # Obtener saldo real de Firestore
    doc_ref = db.collection("usuarios").document(user_info['uid']).get()
    saldo = doc_ref.to_dict().get("saldo", 0) if doc_ref.exists else 0
    
    st.sidebar.metric("Saldo Disponible", f"{saldo} créditos")
    
    if st.sidebar.button("Cerrar Sesión"):
        st.session_state.authenticated = False
        st.session_state.user_data = None
        st.rerun()

    # Contenido principal
    st.title("🚀 Sistema de Consultas Pro")
    st.write("Bienvenido al área restringida. Tu acceso ha sido validado.")
    
    pregunta = st.text_area("Escribe los datos de tu investigación:")
    
    if st.button("Ejecutar Consulta (-1 crédito)"):
        if saldo > 0:
            with st.spinner("Procesando..."):
                # Descontar en Firestore
                db.collection("usuarios").document(user_info['uid']).update({
                    "saldo": firestore.Increment(-1)
                })
                st.success(f"Consulta terminada con éxito. Nuevo saldo: {saldo - 1}")
                st.rerun()
        else:
            st.error("❌ Saldo insuficiente. Contacta a soporte para recargar.")
