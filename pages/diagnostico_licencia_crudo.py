import streamlit as st
import requests

st.set_page_config(page_title="Seeker v6 Oficial", page_icon="🚗")

st.title("🚗 Consulta de Licencia Oficial")
st.markdown("---")

# Configuración según Documentación Oficial
URL = "https://seeker-v6.com/vehiculos/licencia_conductor"
TOKEN = "sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"

col1, col2 = st.columns(2)
with col1:
    dni_input = st.text_input("Número de DNI", value="60799566")
with col2:
    tipo_input = st.selectbox("Tipo de Consulta", ["dni", "licencia"])

if st.button("CONSULTAR AHORA (Costo: 3 Créditos)"):
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }
    
    # Payload exacto como pide la documentación
    payload = {
        "dni": dni_input,
        "tipo": tipo_input
    }
    
    with st.spinner("Conectando con Seeker DataAPI..."):
        try:
            response = requests.post(URL, headers=headers, json=payload, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "success":
                    st.success("✅ Datos recuperados con éxito")
                    st.json(data)
                else:
                    st.error(f"Error de la API: {data.get('message', 'Desconocido')}")
            elif response.status_code == 401:
                st.error("❌ Token inválido o expirado.")
            elif response.status_code == 403:
                st.error("❌ Saldo insuficiente (Costo: 3 créditos).")
            else:
                st.warning(f"Respuesta inesperada (Status: {response.status_code})")
                st.text(response.text)
                
        except Exception as e:
            st.error(f"Error de conexión: {str(e)}")

st.divider()
st.caption("Asegúrate de tener créditos suficientes en tu cuenta de Seeker.")
