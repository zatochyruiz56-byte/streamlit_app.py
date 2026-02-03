import streamlit as st
import requests
import io

st.set_page_config(page_title="Decoder Seeker", layout="centered")

st.title("🪪 Analizador de Licencia (Binarios)")
st.info("Este script detecta si la API envía un JSON, una Imagen o un PDF.")

dni_input = st.text_input("Ingrese DNI", value="60799566")
tipo_input = st.selectbox("Tipo de consulta", ["BÁSICO", "COMPLETO"])

if st.button("EJECUTAR ESCANEO PROFUNDO", type="primary"):
    url = "https://seeker-v6.com/vehiculos/licencia_conductor"
    token = "sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    payload = {"dni": dni_input, "tipo": tipo_input}

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=25)
        
        # 1. Analizar qué tipo de contenido llegó
        content_type = response.headers.get("Content-Type", "").lower()
        
        st.subheader("📡 Diagnóstico de Cabeceras")
        st.write(f"**Status Code:** {response.status_code}")
        // Fix: Added backslash to escape backticks within the template literal string to prevent it from closing early and causing variable resolution errors
        st.write(f"**Tipo de Contenido detectado:** `{content_type}`")

        st.divider()

        # 2. Manejar según el formato
        if "application/json" in content_type:
            st.success("✅ Respuesta JSON detectada")
            st.json(response.json())
            
        elif "image" in content_type:
            st.success("🖼️ ¡Es una IMAGEN!")
            st.image(response.content, caption="Imagen devuelta por la API")
            st.download_button("Descargar Imagen", response.content, "licencia.jpg")
            
        elif "pdf" in content_type:
            st.success("📄 ¡Es un documento PDF!")
            st.download_button("📥 DESCARGAR RÉCORD PDF", response.content, "record_conductor.pdf")
            st.info("Haz clic en el botón de arriba para abrir el documento.")
            
        else:
            st.warning(f"⚠️ Formato no reconocido por el navegador: {content_type}")
            # Si no sabemos qué es, intentamos ver los primeros caracteres
            st.text("Vista previa de datos crudos:")
            st.text(response.text[:500])
            
            # Botón de emergencia para guardar lo que sea que llegó
            st.download_button("Descargar respuesta cruda (Unknown)", response.content, "respuesta_api.bin")

    except Exception as e:
        st.error(f"Error técnico: {str(e)}")

st.divider()
st.caption("Si el PDF se descarga vacío o la imagen no carga, avísame para revisar el token o los permisos.")
