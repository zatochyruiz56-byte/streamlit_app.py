import streamlit as st
import requests

if not st.session_state.get('autenticado', False):
    st.warning("⚠️ Acceso no autorizado. Inicie sesión en la página principal.")
    st.stop()

st.title("👤 Consulta de Personas")
st.markdown("---")

# Datos de la API extraídos de tu documentación (Imagen 46f2c6)
TOKEN = "sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"
API_URL = "https://seeker-v6.com/personas/apiPremium/dni"

dni = st.text_input("DNI a consultar (8 dígitos):", max_chars=8)

if st.button("Consultar Ahora"):
    if len(dni) == 8:
        with st.spinner("Conectando con DataAPI..."):
            try:
                headers = {"Authorization": f"Bearer {TOKEN}"}
                payload = {"dni": dni}
                # Usamos data=payload para enviar como form-urlencoded según tu imagen 46f28c
                response = requests.post(API_URL, headers=headers, data=payload)
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("status") == "success":
                        st.success("✅ Datos encontrados")
                        st.json(data.get("data"))
                        st.info(f"Créditos restantes: {data.get('creditos_restantes')}")
                    else:
                        st.error(f"API dice: {data.get('message')}")
                else:
                    st.error(f"Error de conexión: Código {response.status_code}")
            except Exception as e:
                st.error(f"Fallo técnico: {e}")
    else:
        st.warning("Por favor, ingrese un DNI válido de 8 dígitos.")
