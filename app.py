import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth
import requests
import random

# Inicialización de Firebase
if not firebase_admin._apps:
    fb_dict = dict(st.secrets["firebase"])
    fb_dict["private_key"] = fb_dict["private_key"].replace('\\n', '\n')
    cred = credentials.Certificate(fb_dict)
    firebase_admin.initialize_app(cred)

def send_otp(email, code):
    url = "https://api.resend.com/emails"
    headers = {
        "Authorization": f"Bearer {st.secrets['resend_api_key']}",
        "Content-Type": "application/json"
    }
    payload = {
        "from": "ZTCHY PRO <onboarding@resend.dev>",
        "to": [email],
        "subject": "Código de Verificación ZTCHY",
        "html": f"<h2>Tu código es: {code}</h2>"
    }
    return requests.post(url, json=payload, headers=headers)

# Interfaz de Usuario
st.title("Registro ZTCHY-PRO")

if "step" not in st.session_state: 
    st.session_state.step = "registro"

if st.session_state.step == "registro":
    email = st.text_input("Ingresa tu correo (Debe ser el tuyo en modo prueba)")
    password = st.text_input("Contraseña", type="password")
    
    if st.button("Enviar Código"):
        if email != "zatochyruiz56@gmail.com":
            st.error("⚠️ En modo prueba de Resend, solo puedes enviarte correos a TI mismo (zatochyruiz56@gmail.com).")
        else:
            st.session_state.generated_code = str(random.randint(100000, 999999))
            st.session_state.user_data = {"email": email, "password": password}
            
            response = send_otp(email, st.session_state.generated_code)
            if response.status_code in [200, 201, 202]:
                st.success("✅ Código enviado. Revisa tu correo.")
                st.session_state.step = "verificacion"
                st.rerun()
            else:
                st.error(f"Error al enviar: {response.text}")

elif st.session_state.step == "verificacion":
    code_input = st.text_input("Ingresa el código de 6 dígitos")
    if st.button("Validar y Crear Cuenta"):
        if code_input == st.session_state.generated_code:
            try:
                auth.create_user(
                    email=st.session_state.user_data["email"],
                    password=st.session_state.user_data["password"]
                )
                st.success("🎉 ¡Cuenta creada con éxito! Ya puedes entrar.")
                st.session_state.step = "registro"
            except Exception as e:
                st.error(f"Error de Firebase: {e}")
        else:
            st.error("❌ Código incorrecto")
