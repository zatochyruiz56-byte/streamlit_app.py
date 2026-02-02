import streamlit as st
import requests

# Seguridad: Si no está logueado, no entra
if not st.session_state.get('auth', False):
    st.warning("Inicie sesión en la página principal.")
    st.stop()

st.title("👤 Consulta de Personas")
st.markdown("---")

# Espacio para la consulta
dni = st.text_input("Ingrese el DNI a consultar:", max_chars=8)

if st.button("CONSULTAR"):
    if len(dni) == 8:
        # Configuración de tu API
        TOKEN = "sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"
        URL = "https://seeker-v6.com/personas/apiPremium/dni"
        
        with st.spinner("Buscando en DataAPI..."):
            try:
                # Enviamos la petición
                response = requests.post(URL, headers={"Authorization": f"Bearer {TOKEN}"}, data={"dni": dni})
                
                if response.status_code == 200:
                    data = response.json()
                    st.success("✅ Resultados:")
                    # Muestra la info que manda la API
                    st.json(data) 
                else:
                    st.error(f"Error de API: {response.status_code}")
            except Exception as e:
                st.error(f"Error de conexión: {e}")
    else:
        st.warning("El DNI debe tener 8 dígitos.")

if st.button("🔙 Volver al Panel"):
    st.switch_page("app.py")
