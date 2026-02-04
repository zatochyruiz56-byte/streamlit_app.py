import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth, firestore
import requests
import random

# Inicialización de Firebase con Firestore
if not firebase_admin._apps:
    fb_dict = dict(st.secrets["firebase"])
    fb_dict["private_key"] = fb_dict["private_key"].replace('\\n', '\n')
    cred = credentials.Certificate(fb_dict)
    firebase_admin.initialize_app(cred)

db = firestore.client()

def send_otp(email, code):
    url = "https://api.mailersend.com/v1/email"
    headers = {
        "Authorization": f"Bearer {st.secrets['mailersend_api_key']}",
        "Content-Type": "application/json",
        "X-Requested-With": "XMLHttpRequest"
    }
    payload = {
        "from": {"email": f"MS_ALHbS4@{st.secrets['mailersend_domain']}"},
        "to": [{"email": email}],
        "subject": "Código de Verificación ZTCHY",
        "html": f"<h2>Tu código es: {code}</h2>",
        "text": f"Tu código es: {code}"
    }
    return requests.post(url, json=payload, headers=headers)

# --- LÓGICA DE NAVEGACIÓN ---
if "user" not in st.session_state:
    st.session_state.user = None

if "page" not in st.session_state:
    st.session_state.page = "login"

# --- FUNCIONES DE SALDO ---
def get_balance(uid):
    user_ref = db.collection("usuarios").document(uid)
    doc = user_ref.get()
    if doc.exists:
        return doc.to_dict().get("saldo", 0)
    return 0

def update_balance(uid, amount):
    user_ref = db.collection("usuarios").document(uid)
    user_ref.update({"saldo": firestore.Increment(amount)})

# --- PANTALLA DE LOGIN ---
if st.session_state.page == "login":
    st.title("Iniciar Sesión")
    email_login = st.text_input("Correo")
    pass_login = st.text_input("Contraseña", type="password")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Entrar"):
            try:
                # Nota: El SDK de Admin no valida contraseñas directamente. 
                # En producción se usa Firebase Auth REST API o el SDK de cliente.
                user = auth.get_user_by_email(email_login)
                st.session_state.user = {"email": user.email, "uid": user.uid}
                st.session_state.page = "consulta"
                st.rerun()
            except Exception:
                st.error("Credenciales inválidas o usuario no encontrado.")
    with col2:
        if st.button("Crear cuenta"):
            st.session_state.page = "registro"
            st.rerun()

# --- PANTALLA DE REGISTRO ---
elif st.session_state.page == "registro":
    st.title("Registro ZTCHY-PRO")
    email_reg = st.text_input("Ingresa tu correo")
    pass_reg = st.text_input("Crea una contraseña", type="password")
    
    if st.button("Enviar Código"):
        st.session_state.generated_code = str(random.randint(100000, 999999))
        st.session_state.temp_data = {"email": email_reg, "password": pass_reg}
        send_otp(email_reg, st.session_state.generated_code)
        st.info("Código enviado.")
        st.session_state.page = "validar_otp"
        st.rerun()

elif st.session_state.page == "validar_otp":
    otp_input = st.text_input("Código de 6 dígitos")
    if st.button("Finalizar Registro"):
        if otp_input == st.session_state.generated_code:
            user = auth.create_user(
                email=st.session_state.temp_data["email"],
                password=st.session_state.temp_data["password"]
            )
            # Inicializar saldo (Ejemplo: 10 créditos gratis al unirse)
            db.collection("usuarios").document(user.uid).set({
                "email": user.email,
                "saldo": 10
            })
            st.success("Cuenta creada con 10 créditos de regalo. Inicia sesión.")
            st.session_state.page = "login"
            st.rerun()

# --- PANTALLA DE CONSULTA (PROTEGIDA) ---
elif st.session_state.page == "consulta":
    if not st.session_state.user:
        st.session_state.page = "login"
        st.rerun()

    st.sidebar.write(f"Usuario: {st.session_state.user['email']}")
    saldo_actual = get_balance(st.session_state.user['uid'])
    st.sidebar.metric("Saldo Disponible", f"{saldo_actual} créditos")
    
    if st.sidebar.button("Cerrar Sesión"):
        st.session_state.user = None
        st.session_state.page = "login"
        st.rerun()

    st.title("Consultas ZTCHY-PRO")
    query = st.text_input("¿Qué deseas consultar?")
    
    if st.button("Realizar Consulta (-1 crédito)"):
        if saldo_actual > 0:
            with st.spinner("Procesando consulta..."):
                # Aquí va tu lógica de consulta (API, búsqueda, etc.)
                update_balance(st.session_state.user['uid'], -1)
                st.success(f"Consulta exitosa. Tu nuevo saldo es {saldo_actual - 1}")
        else:
            st.error("❌ Saldo insuficiente. Por favor recarga créditos.")
