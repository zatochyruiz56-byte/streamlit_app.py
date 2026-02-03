import streamlit as st
import requests
import json

def run():
    st.title("📲 Titularidad Online - Diagnóstico Total")
    st.markdown("---")

    # Parámetros de conexión
    API_URL = "https://seeker-v6.com/telefonos/titularidad"
    TOKEN = "sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"

    # Input con placeholder genérico
    dni = st.text_input("Ingrese DNI para consulta", max_chars=8, placeholder="Ejm: 12345678")

    if st.button("🚀 EJECUTAR Y CAPTURAR RESPUESTA"):
        if not dni:
            st.warning("Escriba un DNI primero.")
            return

        headers = {
            "Authorization": f"Bearer {TOKEN}",
            "Content-Type": "application/json"
        }
        
        # Probamos con 'doc' como pediste
        payload = {"doc": dni}

        try:
            with st.spinner("Llamando a la API..."):
                response = requests.post(API_URL, json=payload, headers=headers)
            
            # --- ZONA DE ANÁLISIS ---
            st.subheader("🛰️ Informe del Servidor")
            
            # 1. Código de Estado HTTP
            status_code = response.status_code
            if status_code == 200:
                st.success(f"Código HTTP: {status_code} (Conexión Exitosa)")
            else:
                st.error(f"Código HTTP: {status_code} (El servidor rechazó la petición)")

            # 2. Tipo de Contenido (Aquí descubrimos el error)
            content_type = response.headers.get("Content-Type", "")
            st.write(f"**Tipo de archivo recibido:** `{content_type}`")

            st.markdown("---")

            # 3. Intento de mostrar JSON o mostrar Texto Crudo
            if "application/json" in content_type:
                try:
                    data = response.json()
                    st.markdown("### ✅ JSON Recibido:")
                    st.json(data)
                except Exception as json_err:
                    st.error("El encabezado dice JSON pero el contenido no lo es.")
                    st.code(response.text)
            else:
                st.warning("⚠️ El servidor NO envió un JSON. Envió una página web o un error de texto.")
                st.markdown("### 📄 Contenido de la respuesta (Raw Text):")
                # Mostramos el HTML/Texto crudo para ver el error real
                st.code(response.text, language="html")

        except Exception as e:
            st.error(f"🔥 Error de conexión (Python): {str(e)}")

if __name__ == "__main__":
    run()
