import streamlit as st
import requests

# SEGURIDAD: Verifica si el usuario inició sesión en app.py
if not st.session_state.get('autenticado', False):
    st.error("⚠️ Por favor, inicia sesión en la página principal.")
    st.stop()

st.title("👤 Consulta de Personas")
st.markdown("---")

# Selección de sub-ramas
opcion = st.radio("Seleccione el servicio:", ["DNI Premium", "DNI Básico", "Nombres"], horizontal=True)

# Configuración de tu API
TOKEN = "sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"
API_URL = "https://seeker-v6.com/personas/apiPremium/dni"

if opcion == "DNI Premium":
    st.subheader("💳 Servicio Premium")
    dni_input = st.text_input("Ingrese el número de DNI:", max_chars=8)
    
    if st.button("Consultar Ahora"):
        if len(dni_input) == 8:
            with st.spinner("Buscando información..."):
                try:
                    # Formato de envío que ya probamos y funcionó
                    headers = {"Authorization": f"Bearer {TOKEN}"}
                    payload = {"dni": dni_input}
                    
                    response = requests.post(API_URL, headers=headers, data=payload)
                    data = response.json()
                    
                    if data.get("status") == "success":
                        st.success("✅ Datos encontrados")
                        st.json(data.get("data")) # Muestra los resultados
                        st.info(f"⚡ Créditos restantes: {data.get('creditos_restantes')}")
                    else:
                        st.error(f"Error: {data.get('message')}")
                        
                except Exception as e:
                    st.error(f"Fallo de conexión: {e}")
        else:
            st.warning("El DNI debe tener 8 números.")

elif opcion == "DNI Básico":
    st.info("Módulo en desarrollo.")

elif opcion == "Nombres":
    st.info("Módulo en desarrollo.")
