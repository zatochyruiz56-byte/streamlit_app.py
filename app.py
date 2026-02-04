import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth, firestore
import requests
import random

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="ZTCHY PRO", layout="centered")

# Inyección de CSS para fondo de Machu Picchu y control de visibilidad
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), 
                    url("https://images.unsplash.com/photo-1526392060635-9d6019884377?q=80&w=2070&auto=format&fit=crop");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    [data-testid="stSidebar"] {
        display: """ + ("block" if st.session_state.get('authenticated') else "none") + """;
    }
    .auth-container {
        background-color: rgba(255, 255, 255, 0.95);
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0px 10px 30px rgba(0,0,0,0.5);
        color: black;
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
    headers = {"Authorization": f"Bearer {st.secrets['mailersend_api_key']}", "Content-Type": "application/json"}
    payload = {
        "from": {"email": f"MS_ALHbS4@{st.secrets['mailersend_domain']}"},
        "to": [{"email": email}],
        "subject": "Código de Registro ZTCHY",
        "html": f"<h2>Tu código es: {code}</h2>"
    }
    return requests.post(url, json=payload, headers=headers)

# --- MANEJO DE ESTADO ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "page" not in st.session_state:
    st.session_state.page = "login"

# --- INTERFAZ ---

if not st.session_state.authenticated:
    st.markdown('<div class="auth-container">', unsafe_allow_html=True)
    
    if st.session_state.page == "login":
        st.title("🏔️ ZTCHY PRO")
        email = st.text_input("Correo")
        password = st.text_input("Contraseña", type="password")
        
        if st.button("Iniciar Sesión", use_container_width=True):
            try:
                user = auth.get_user_by_email(email)
                st.session_state.authenticated = True
                st.session_state.user_data = {"uid": user.uid, "email": user.email}
                st.rerun()
            except:
                st.error("Credenciales incorrectas o usuario no encontrado.")
        
        if st.button("Crear cuenta", use_container_width=True):
            st.session_state.page = "registro"
            st.rerun()

    elif st.session_state.page == "registro":
        st.title("📝 Registro")
        reg_email = st.text_input("Ingresa tu correo")
        reg_pass = st.text_input("Crea una contraseña", type="password")
        
        if st.button("Enviar Código OTP", use_container_width=True):
            if reg_email and reg_pass:
                st.session_state.generated_otp = str(random.randint(100000, 999999))
                # AQUÍ CORREGIMOS EL NOMBRE PARA QUE NO DE ERROR
                st.session_state.temp_reg_data = {"email": reg_email, "pass": reg_pass}
                send_otp(reg_email, st.session_state.generated_otp)
                st.session_state.page = "verificar"
                st.rerun()
            else:
                st.warning("Completa todos los campos.")

    elif st.session_state.page == "verificar":
        st.title("🛡️ Verificación")
        code_in = st.text_input("Código de 6 dígitos")
        if st.button("Validar Registro", use_container_width=True):
            if code_in == st.session_state.generated_otp:
                # Usamos los datos guardados en el paso anterior
                email_final = st.session_state.temp_reg_data["email"]
                pass_final = st.session_state.temp_reg_data["pass"]
                
                user = auth.create_user(email=email_final, password=pass_final)
                
                # CREAR SALDO EN FIRESTORE
                db.collection("usuarios").document(user.uid).set({
                    "email": user.email,
                    "saldo": 10
                })
                
                st.success("¡Cuenta creada con 10 créditos! Inicia sesión.")
                st.session_state.page = "login"
                st.rerun()
            else:
                st.error("Código incorrecto.")
    
    st.markdown('</div>', unsafe_allow_html=True)

else:
    # PANEL PRINCIPAL (SÓLO SI ESTÁ AUTENTICADO)
    st.sidebar.title("Panel ZTCHY")
    st.sidebar.write(f"Usuario: {st.session_state.user_data['email']}")
    
    # Consultar saldo real de Firestore
    doc = db.collection("usuarios").document(st.session_state.user_data['uid']).get()
    saldo_actual = doc.to_dict().get("saldo", 0) if doc.exists else 0
    
    st.sidebar.metric("Saldo Disponible", f"{saldo_actual} créditos")
    
    if st.sidebar.button("Cerrar Sesión"):
        st.session_state.authenticated = False
        st.rerun()

    st.title("🔍 Sistema de Consultas")
    consulta = st.text_input("Haz tu pregunta aquí...")
    
    if st.button("Consultar (-1 crédito)"):
        if saldo_actual > 0:
            with st.spinner("Descontando saldo..."):
                db.collection("usuarios").document(st.session_state.user_data['uid']).update({
                    "saldo": firestore.Increment(-1)
                })
                st.success("Consulta exitosa.")
                st.rerun()
        else:
            st.error("Sin créditos suficientes.")
