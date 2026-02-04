import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth, firestore
import requests
import random

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="ZTCHY PRO", layout="centered")

# Inyección de CSS para el fondo de Machu Picchu y diseño
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), 
                    url("https://images.unsplash.com/photo-1526392060635-9d6019884377?q=80&w=2070&auto=format&fit=crop");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    .auth-container {
        background-color: rgba(255, 255, 255, 0.9);
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.3);
    }
    [data-testid="stSidebar"] {
        display: """ + ("block" if st.session_state.get('authenticated') else "none") + """;
    }
    </style>
    """, unsafe_allow_html=True)

# --- INICIALIZACIÓN DE FIREBASE ---
if not firebase_admin._apps:
    fb_dict = dict(st.secrets["firebase"])
    fb_dict["private_key"] = fb_dict["private_key"].replace('\\n', '\n')
    cred = credentials.Certificate(fb_dict)
    firebase_admin.initialize_app(cred)

db = firestore.client()

# --- FUNCIONES ---
def send_otp(email, code):
    url = "https://api.mailersend.com/v1/email"
    headers = {
        "Authorization": f"Bearer {st.secrets['mailersend_api_key']}",
        "Content-Type": "application/json"
    }
    payload = {
        "from": {"email": f"MS_ALHbS4@{st.secrets['mailersend_domain']}"},
        "to": [{"email": email}],
        "subject": "Código de Verificación ZTCHY",
        "html": f"<h2>Tu código es: {code}</h2>"
    }
    return requests.post(url, json=payload, headers=headers)

def get_balance(uid):
    doc = db.collection("usuarios").document(uid).get()
    return doc.to_dict().get("saldo", 0) if doc.exists else 0

# --- LÓGICA DE ESTADO ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "page" not in st.session_state:
    st.session_state.page = "login"

# --- INTERFAZ DE USUARIO ---

# 1. SI NO ESTÁ AUTENTICADO: MURO DE LOGIN/REGISTRO
if not st.session_state.authenticated:
    with st.container():
        st.markdown('<div class="auth-container">', unsafe_allow_html=True)
        
        if st.session_state.page == "login":
            st.title("🏔️ ZTCHY PRO - Ingreso")
            email = st.text_input("Correo electrónico")
            password = st.text_input("Contraseña", type="password")
            
            if st.button("Iniciar Sesión", use_container_width=True):
                try:
                    user = auth.get_user_by_email(email)
                    # En este punto el usuario existe. 
                    # st.success(f"Bienvenido {user.email}")
                    st.session_state.authenticated = True
                    st.session_state.user = {"uid": user.uid, "email": user.email}
                    st.rerun()
                except:
                    st.error("Credenciales incorrectas o cuenta inexistente.")
            
            if st.button("Crear cuenta nueva", variant="secondary"):
                st.session_state.page = "registro"
                st.rerun()

        elif st.session_state.page == "registro":
            st.title("📝 Registro Nuevo")
            reg_email = st.text_input("Tu correo")
            reg_pass = st.text_input("Crea una contraseña", type="password")
            
            if st.button("Enviar Código OTP", use_container_width=True):
                st.session_state.otp = str(random.randint(100000, 999999))
                st.session_state.temp_user = {"email": reg_email, "pass": reg_pass}
                send_otp(reg_email, st.session_state.otp)
                st.session_state.page = "otp"
                st.rerun()
            
            if st.button("Volver al Login"):
                st.session_state.page = "login"
                st.rerun()

        elif st.session_state.page == "otp":
            st.title("🛡️ Verificación")
            code_in = st.text_input("Ingresa el código enviado a tu correo")
            if st.button("Validar y Finalizar"):
                if code_in == st.session_state.otp:
                    user = auth.create_user(
                        email=st.session_state.temp_user["email"],
                        password=st.session_state.temp_user["pass"]
                    )
                    # Crear documento inicial con saldo de regalo (10)
                    db.collection("usuarios").document(user.uid).set({
                        "email": user.email,
                        "saldo": 10
                    })
                    st.success("¡Cuenta creada! Ahora inicia sesión.")
                    st.session_state.page = "login"
                    st.rerun()
                else:
                    st.error("Código incorrecto")
        
        st.markdown('</div>', unsafe_allow_html=True)

# 2. SI ESTÁ AUTENTICADO: PANEL PRINCIPAL
else:
    # Sidebar con Saldo y Usuario
    st.sidebar.title("Panel ZTCHY")
    st.sidebar.write(f"👤 {st.session_state.user['email']}")
    
    saldo = get_balance(st.session_state.user['uid'])
    st.sidebar.metric("Saldo Disponible", f"{saldo} créditos")
    
    if st.sidebar.button("Cerrar Sesión"):
        st.session_state.authenticated = False
        st.session_state.user = None
        st.rerun()

    # Contenido de la Aplicación
    st.title("🚀 Consultas Pro")
    st.write("Bienvenido al área exclusiva.")
    
    input_data = st.text_area("Ingresa los datos para la consulta:")
    
    if st.button("Ejecutar Consulta (-1 crédito)"):
        if saldo > 0:
            with st.spinner("Procesando..."):
                # Restar saldo en la base de datos
                db.collection("usuarios").document(st.session_state.user['uid']).update({
                    "saldo": firestore.Increment(-1)
                })
                # AQUÍ EJECUTAS TU LÓGICA DE NEGOCIO
                st.success(f"Consulta finalizada con éxito. Nuevo saldo: {saldo - 1}")
        else:
            st.error("❌ Saldo insuficiente. Contacta con el administrador.")
