import streamlit as st
import requests

st.set_page_config(page_title="Consulta DNI Premium", page_icon="💳")
st.title("💳 Consulta DNI Premium")

# Configuración de tu API (Imagen 1)
API_URL = "https://seeker-v6.com/api/v1/personas/apiPremium/dni"
TOKEN = "sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"

dni = st.text_input("Ingresa el DNI (8 dígitos):", max_chars=8)

if st.button("Consultar Información"):
    if len(dni) == 8:
        headers = {"Authorization": f"Bearer {TOKEN}"}
        payload = {"dni": dni}
        with st.spinner("Buscando en la base de datos..."):
            try:
                # Al ejecutarse en el servidor, NO hay bloqueo de CORS
                response = requests.post(API_URL, headers=headers, data=payload)
                data = response.json()
                if data.get("status") == "success":
                    st.success("¡Datos encontrados!")
                    st.json(data.get("data"))
                    st.metric("Créditos restantes", data.get("creditos_restantes"))
                else:
                    st.error(f"Error: {data.get('message')}")
            except Exception as e:
                st.error(f"Hubo un fallo: {e}")
    else:
        st.warning("Escribe un DNI válido de 8 dígitos.")
