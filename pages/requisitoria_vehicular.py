import streamlit as st
import requests

def run():
    st.title("🚓 Diagnóstico: Requisitoria Vehicular")
    
    API_URL = "https://seeker-v6.com/personas/requisitorias_vehiculares"
    TOKEN = "sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"

    placa = st.text_input("Placa para prueba", placeholder="ABC123")

    if st.button("🔍 ANALIZAR RESPUESTA"):
        headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
        # Enviamos los parámetros tal cual pide tu documentación
        payload = {"placa": placa, "version": "v1"}

        try:
            response = requests.post(API_URL, json=payload, headers=headers)
            
            st.subheader("📡 Informe Técnico")
            st.write(f"**Código HTTP:** `{response.status_code}`")
            
            # Verificamos si es JSON o HTML
            content_type = response.headers.get("Content-Type", "")
            st.write(f"**Tipo de contenido:** `{content_type}`")

            if "application/json" in content_type:
                st.success("El servidor respondió en formato JSON:")
                st.json(response.json())
            else:
                st.error("⚠️ EL SERVIDOR ENVIÓ UNA PÁGINA HTML (BLOQUEO)")
                st.info("Aquí abajo verás el motivo real del error:")
                # Mostramos el HTML crudo para leer el mensaje de error del proveedor
                st.code(response.text, language="html")

        except Exception as e:
            st.error(f"Error de conexión: {e}")

if __name__ == "__main__":
    run()
