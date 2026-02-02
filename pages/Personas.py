import streamlit as st
import requests

# SEGURIDAD: Verifica si el usuario inició sesión en app.py
if not st.session_state.get('autenticado', False):
    st.error("⚠️ Por favor, inicia sesión en la página principal.")
    st.stop()

st.title("👤 Módulo de Personas")
st.markdown("---")

# Sub-menú para diferentes tipos de consulta
opcion = st.radio("Seleccione el servicio:", ["DNI Premium", "DNI Básico", "Nombres"], horizontal=True)

# Configuración de tu API
TOKEN = "sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"
API_URL = "https://seeker-v6.com/personas/apiPremium/dni"

if opcion == "DNI Premium":
    st.subheader("💳 Consulta DNI Premium")
    dni_input = st.text_input("Ingrese el número de DNI (8 dígitos):", max_chars=8)
    
    if st.button("Consultar Ahora"):
        if len(dni_input) == 8:
            with st.spinner("Buscando en la base de datos..."):
                try:
                    # Formato de envío (Headers + Data)
                    headers = {"Authorization": f"Bearer {TOKEN}"}
                    payload = {"dni": dni_input}
                    
                    response = requests.post(API_URL, headers=headers, data=payload)
                    
                    if response.status_code == 200:
                        data = response.json()
                        if data.get("status") == "success":
                            st.success("✅ Datos encontrados")
                            st.json(data.get("data")) # Muestra los resultados detallados
                            st.info(f"⚡ Créditos restantes: {data.get('creditos_restantes')}")
                        else:
                            st.error(f"Error: {data.get('message')}")
                    else:
                        st.error(f"Error del servidor (Código {response.status_code})")
                        
                except Exception as e:
                    st.error(f"Fallo de conexión: {e}")
        else:
            st.warning("Escriba un DNI válido de 8 números.")

elif opcion == "DNI Básico":
    st.info("Este módulo se conectará a la API de DNI Básico próximamente.")

elif opcion == "Nombres":
    st.info("Este módulo permitirá búsquedas por nombres y apellidos próximamente.")
