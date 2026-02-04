import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth
import requests
import random

# Inicialización de Firebase
if not firebase_admin._apps:
    fb_dict = dict(st.secrets["firebase"])
    # El reemplazo de \n es vital para que no falle el certificado
    fb_dict["private_key"] = fb_dict["private_key"].replace('\\n', '\n')
    cred = credentials.Certificate(fb_dict)
    firebase_admin.initialize_app(cred)

def send_otp(email, code):
    # URL y configuración específica para MailerSend
    url = "https://api.mailersend.com/v1/email"
    headers = {
        "Authorization": f"Bearer {st.secrets['mailersend_api_key']}",
        "Content-Type": "application/json",
        "X-Requested-With": "XMLHttpRequest"
    }
    payload = {
        "from": {
            "email": f"MS_ALHbS4@{st.secrets['mailersend_domain']}"
        },
        "to": [
            {
                "email": email
            }
        ],
        "subject": "Código de Verificación ZTCHY",
        "html": f"<h2>Tu código de verificación es: <b>{code}</b></h2>",
        "text": f"Tu código de verificación es: {code}"
    }
    return requests.post(url, json=payload, headers=headers)

# Interfaz de Usuario
st.title("Registro ZTCHY-PRO")

if "step" not in st.session_state: 
    st.session_state.step = "registro"

if st.session_state.step == "registro":
    email = st.text_input("Ingresa tu correo")
    password = st.text_input("Contraseña", type="password")
    
    if st.button("Enviar Código"):
        # Generar código y guardar datos temporalmente
        st.session_state.generated_code = str(random.randint(100000, 999999))
        st.session_state.user_data = {"email": email, "password": password}
        
        with st.spinner("Enviando código..."):
            response = send_otp(email, st.session_state.generated_code)
            
            # MailerSend devuelve 202 si el envío es aceptado
            if response.status_code in [200, 201, 202]:
                st.success("✅ Código enviado. Revisa tu bandeja de entrada o spam.")
                st.session_state.step = "verificacion"
                st.rerun()
            else:
                st.error(f"Error al enviar: {response.status_code} - {response.text}")

elif st.session_state.step == "verificacion":
    st.write(f"Código enviado a: **{st.session_state.user_data['email']}**")
    code_input = st.text_input("Ingresa el código de 6 dígitos")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Validar y Crear Cuenta"):
            if code_input == st.session_state.generated_code:
                try:
                    auth.create_user(
                        email=st.session_state.user_data["email"],
                        password=st.session_state.user_data["password"]
                    )
                    st.success("🎉 ¡Cuenta creada con éxito!")
                    st.session_state.step = "registro"
                except Exception as e:
                    st.error(f"Error de Firebase: {e}")
            else:
                st.error("❌ Código incorrecto")
    with col2:
        if st.button("Regresar"):
            st.session_state.step = "registro"
            st.rerun()
