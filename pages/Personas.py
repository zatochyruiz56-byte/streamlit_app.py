import streamlit as st
import requests

if not st.session_state.get('autenticado', False):
    st.warning("Por favor regrese al inicio para loguearse.")
    st.stop()

st.title("👤 Consulta de Personas")

TOKEN = "sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"
API_URL = "https://seeker-v6.com/personas/apiPremium/dni"

dni = st.text_input("DNI a consultar:", max_chars=8)

if st.button("Consultar Ahora"):
    if len(dni) == 8:
        with st.spinner("Buscando..."):
            try:
                # El formato que ya vimos que funciona en tu API
                h = {"Authorization": f"Bearer {TOKEN}"}
                d = {"dni": dni}
                res = requests.post(API_URL, headers=h, data=d)
                
                if res.status_code == 200:
                    data = res.json()
                    if data.get("status") == "success":
                        st.success("✅ Datos encontrados")
                        st.json(data.get("data"))
                    else:
                        st.error(data.get("message"))
                else:
                    st.error(f"Error de servidor: {res.status_code}")
            except Exception as e:
                st.error(f"Error de conexión: {e}")
    else:
        st.warning("El DNI debe tener 8 dígitos.")
