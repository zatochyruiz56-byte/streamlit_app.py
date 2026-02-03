import streamlit as st
import requests
import json

st.set_page_config(page_title="JSON Crudo Licencia", layout="centered")

st.title("🪪 Verificador de Información Cruda")
st.info("Este script enviará una petición POST y mostrará exactamente qué información devuelve la API.")

# Configuración de entrada
dni_input = st.text_input("Ingrese DNI para la prueba", value="12345678")
tipo_input = st.selectbox("Tipo de consulta", ["BÁSICO", "COMPLETO"])

if st.button("OBTENER JSON CRUDO", type="primary"):
    url = "https://seeker-v6.com/vehiculos/licencia_conductor"
    token = "sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "dni": dni_input,
        "tipo": tipo_input
    }

    with st.spinner("Conectando con la API..."):
        try:
            # Enviamos como JSON según lo solicitado
            response = requests.post(url, headers=headers, json=payload, timeout=15)
            
            st.subheader("📡 Respuesta del Servidor")
            st.code(f"Status: {response.status_code}")
            
            # Intentamos obtener el JSON
            try:
                raw_data = response.json()
                st.write("### 📄 Contenido JSON Recibido:")
                st.json(raw_data)
                
                # También lo imprimimos como texto crudo por si hay caracteres extraños
                st.write("### 📝 Texto Plano (Raw Text):")
                st.text(response.text)
                
            except Exception as e:
                st.error("La respuesta no es un JSON válido")
                st.text(response.text)
                
        except Exception as e:
            st.error(f"Error de conexión: {str(e)}")

st.divider()
st.caption("Pega este código en tu archivo de Streamlit y ejecuta para ver la información.")
