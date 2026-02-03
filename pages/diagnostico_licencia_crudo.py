import streamlit as st
import requests
import json

st.set_page_config(page_title="Seeker Binary Debugger", layout="centered")

st.title("🪪 Analizador de Licencia Cruda")
st.write("Usa este script para ver si la API te está enviando una Imagen, un PDF o un JSON.")

dni_input = st.text_input("DNI del Conductor", value="60799566")
tipo_input = st.selectbox("Nivel de Detalle", ["BÁSICO", "COMPLETO"])

if st.button("EXTRAER INFORMACIÓN AHORA", type="primary"):
    url = "https://seeker-v6.com/vehiculos/licencia_conductor"
    token = "sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    payload = {"dni": dni_input, "tipo": tipo_input}

    with st.status("Consultando Servidor Seeker...", expanded=True) as status:
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            
            # Analizar el tipo de contenido que llega
            content_type = response.headers.get("Content-Type", "").lower()
            
            st.subheader("📡 Informe de Respuesta")
            st.code(f"Código HTTP: {response.status_code}")
            st.info(f"Tipo de Datos Recibidos: {content_type}")

            if response.status_code == 200:
                status.update(label="✅ Datos capturados correctamente", state="complete")
                
                # Caso 1: Es un JSON (Texto de datos)
                if "application/json" in content_type:
                    st.success("Se recibió un paquete de datos JSON")
                    st.json(response.json())
                
                # Caso 2: Es una Imagen (Foto del carnet/conductor)
                elif "image" in content_type:
                    st.success("Se recibió una IMAGEN binaria")
                    st.image(response.content, caption="Vista previa del resultado")
                    st.download_button("Descargar Imagen", response.content, "resultado.jpg")
                
                # Caso 3: Es un PDF (Récord oficial)
                elif "pdf" in content_type:
                    st.success("Se recibió un documento PDF")
                    st.download_button("📥 DESCARGAR DOCUMENTO PDF", response.content, "record_conductor.pdf")
                    st.info("Haz clic arriba para abrir el archivo.")
                
                # Caso 4: Desconocido (Error de formato o HTML)
                else:
                    st.warning("El formato no es estándar. Mostrando vista previa:")
                    st.text(response.text[:1000])
                    st.download_button("Descargar Archivo Crudo", response.content, "respuesta_desconocida.bin")
            else:
                status.update(label="❌ Error en la API", state="error")
                st.error(f"Error {response.status_code}: {response.text}")

        except Exception as e:
            status.update(label="💥 Fallo de Conexión", state="error")
            st.error(f"Error técnico: {str(e)}")

st.divider()
st.caption("Script optimizado para evitar SyntaxErrors en Streamlit Cloud.")
