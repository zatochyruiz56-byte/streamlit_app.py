import streamlit as st
import requests

# Validación de sesión
if not st.session_state.get('autenticado', False):
    st.error("Inicie sesión en la página principal.")
    st.stop()

st.title("👤 Consulta de Personas")

TOKEN = "sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"
API_URL = "https://seeker-v6.com/personas/apiPremium/dni"

dni = st.text_input("DNI (8 dígitos):", max_chars=8)

if st.button("Consultar Premium"):
    if len(dni) == 8:
        with st.spinner("Consultando..."):
            try:
                res = requests.post(API_URL, headers={"Authorization": f"Bearer {TOKEN}"}, data={"dni": dni})
                data = res.json()
                if data.get("status") == "success":
                    st.success("✅ Datos encontrados")
                    st.json(data.get("data"))
                else:
                    st.error(data.get("message"))
            except Exception as e:
                st.error(f"Error de conexión: {e}")
    else:
        st.warning("Ingrese un DNI válido.")
