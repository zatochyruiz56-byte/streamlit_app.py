import streamlit as st
import requests

# Validar sesión
if not st.session_state.get('autenticado', False):
    st.error("Acceso denegado. Por favor inicie sesión.")
    st.stop()

st.title("👤 Módulo de Personas")

# Datos de la API (Imagen 46f2c6)
TOKEN = "sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"
API_URL = "https://seeker-v6.com/personas/apiPremium/dni"

dni = st.text_input("Ingrese DNI a consultar:", max_chars=8)

if st.button("Ejecutar Consulta"):
    if len(dni) == 8:
        with st.spinner("Consultando base de datos..."):
            try:
                headers = {"Authorization": f"Bearer {TOKEN}"}
                payload = {"dni": dni}
                # Enviamos como data (form-urlencoded)
                res = requests.post(API_URL, headers=headers, data=payload)
                
                if res.status_code == 200:
                    data = res.json()
                    if data.get("status") == "success":
                        st.success("✅ Datos encontrados")
                        st.json(data.get("data"))
                        st.info(f"Créditos restantes: {data.get('creditos_restantes')}")
                    else:
                        st.error(f"Mensaje: {data.get('message')}")
                else:
                    st.error(f"Error de servidor: {res.status_code}")
            except Exception as e:
                st.error(f"Fallo de conexión: {e}")
    else:
        st.warning("Escriba un DNI de 8 números.")
