import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth, firestore
import requests
import random

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="ZTCHY PRO", layout="centered")

# Inyección de CSS para fondo de Machu Picchu y ocultar sidebar
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), 
                    url("https://images.unsplash.com/photo-1526392060635-9d6019884377?q=80&w=2070&auto=format&fit=crop");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    /* Ocultar sidebar por completo si no está autenticado */
    [data-testid="stSidebar"] {
        display: """ + ("block" if st.session_state.get('authenticated') else "none") + """;
    }
    .auth-box {
        background-color: rgba(255, 255, 255, 0.95);
        padding: 40px;
        border-radius: 20px;
        box-shadow: 0px 10px 25px rgba(0,0,0,0.5);
        color: #1e1e1e;
    }
    </style>
    """, unsafe_allow_html=True)

# --- INICIALIZACIÓN FIREBASE ---
if not firebase_admin._apps:
    fb_dict = dict(st.secrets["firebase"])
    fb_dict["private_key"] = fb_dict["private_key"].replace('\\n', '\n')
    cred = credentials.Certificate(fb_dict)
    firebase_admin.initialize_app(cred)

db = firestore.client()

# --- FUNCIONES ---
def send_otp(email, code):
    url = "https://api.mailersend.com/v1/email"
    headers = {"Authorization": f"Bearer {st.secrets['mailersend_api_key']}", "Content-Type": "application/json"}
    payload = {
        "from": {"email": f"MS_ALHbS4@{st.secrets['mailersend_domain']}"},
        "to": [{"email": email}],
        "subject": "Código ZTCHY PRO",
        "html": f"<h3>Tu código es: {code}</h3>"
    }
    return requests.post(url, json=payload, headers=headers)

# --- LÓGICA DE NAVEGACIÓN ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "page" not in st.session_state:
    st.session_state.page = "login"

# --- VISTAS ---

if not st.session_state.authenticated:
    st.markdown('<div class="auth-box">', unsafe_allow_html=True)
    
    if st.session_state.page == "login":
        st.title("🏔️ ZTCHY PRO")
        st.subheader("Ingresa a tu cuenta")
        email = st.text_input("Correo electrónico")
        password = st.text_input("Contraseña", type="password")
        
        if st.button("Iniciar Sesión", use_container_width=True):
            try:
                user = auth.get_user_by_email(email)
                st.session_state.authenticated = True
                st.session_state.user = {"uid": user.uid, "email": user.email}
                st.rerun()
            except:
                st.error("Usuario no encontrado.")
        
        # ELIMINADO EL PARÁMETRO 'variant' QUE CAUSABA EL ERROR
        if st.button("Crear cuenta nueva", use_container_width=True):
            st.session_state.page = "registro"
            st.rerun()

    elif st.session_state.page == "registro":
        st.title("📝 Registro")
        reg_email = st.text_input("Nuevo correo")
        reg_pass = st.text_input("Nueva contraseña", type="password")
        
        if st.button("Enviar Código de Verificación", use_container_width=True):
            st.session_state.otp = str(random.randint(100000, 999999))
            st.session_state.temp_data = {"email": reg_email, "pass": reg_pass}
            send_otp(reg_email, st.session_state.otp)
            st.session_state.page = "otp_verify"
            st.rerun()
        
        if st.button("Volver", use_container_width=True):
            st.session_state.page = "login"
            st.rerun()

    elif st.session_state.page == "otp_verify":
        st.title("🛡️ Verifica tu correo")
        otp_in = st.text_input("Ingresa el código de 6 dígitos")
        if st.button("Finalizar Registro", use_container_width=True):
            if otp_in == st.session_state.otp:
                user = auth.create_user(
                    email=st.session_state.temp_user["email"],
                    password=st.session_state.temp_user["pass"]
                )
                # Crear saldo inicial en Firestore
                db.collection("usuarios").document(user.uid).set({"email": user.email, "saldo": 10})
                st.success("¡Cuenta creada! Por favor inicia sesión.")
                st.session_state.page = "login"
                st.rerun()
            else:
                st.error("Código incorrecto.")
    
    st.markdown('</div>', unsafe_allow_html=True)

else:
    # SI ESTÁ AUTENTICADO: SE MUESTRA EL PANEL
    st.sidebar.title("Menú Principal")
    st.sidebar.write(f"Usuario: {st.session_state.user['email']}")
    
    # Obtener saldo de Firestore
    user_ref = db.collection("usuarios").document(st.session_state.user['uid']).get()
    saldo = user_ref.to_dict().get("saldo", 0) if user_ref.exists else 0
    
    st.sidebar.metric("Saldo Disponible", f"{saldo} créditos")
    
    if st.sidebar.button("Cerrar Sesión"):
        st.session_state.authenticated = False
        st.rerun()

    st.title("🔍 Sistema de Consultas")
    query = st.text_input("¿Qué deseas investigar hoy?")
    
    if st.button("Consultar (-1 crédito)"):
        if saldo > 0:
            with st.spinner("Procesando consulta..."):
                # Descontar saldo
                db.collection("usuarios").document(st.session_state.user['uid']).update({
                    "saldo": firestore.Increment(-1)
                })
                st.success("Consulta finalizada. Se ha descontado 1 crédito.")
        else:
            st.error("No tienes saldo suficiente.")
