import streamlit as st
import requests

def run():
    st.title("🚗 Consulta SUNARP Básico")
    st.markdown("---")

    # Configuración de API según tu documentación
    API_URL = "https://seeker-v6.com/personas/sunarpbasicoapi"
    TOKEN = "sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"
    
    dni = st.text_input("Ingrese DNI para consulta SUNARP", max_chars=8)

    if st.button("🔍 CONSULTAR PROPIEDADES"):
        if len(dni) == 8:
            headers = {
                "Authorization": f"Bearer {TOKEN}",
                "Content-Type": "application/json"
            }
            payload = {"dni": dni}

            try:
                with st.spinner("Buscando en registros públicos..."):
                    response = requests.post(API_URL, json=payload, headers=headers)
                    
                    # Verificación de tipo de respuesta
                    if "application/json" not in response.headers.get("Content-Type", ""):
                        st.error("❌ El servidor no respondió con datos (Posible error de sesión).")
                        return

                    data = response.json()

                if response.status_code == 200 and data.get("status") == "success":
                    st.success("✅ Información recuperada")
                    
                    # Renderizado de los datos reales de SUNARP
                    resultado = data.get("data")
                    if resultado:
                        st.subheader("📋 Resultados SUNARP")
                        st.json(resultado) 
                    else:
                        st.info("No se encontraron propiedades o vehículos registrados para este DNI.")
                    
                    if "creditos_restantes" in data:
                        st.sidebar.metric("Saldo", f"{data['creditos_restantes']} 🪙")
                else:
                    # Capturamos el error exacto de la API
                    error_msg = data.get("message", "Error desconocido")
                    st.error(f"⚠️ Error de la API: {error_msg}")

            except Exception as e:
                st.error(f"🔥 Error de conexión: {str(e)}")
        else:
            st.warning("Ingrese un DNI válido de 8 dígitos.")

if __name__ == "__main__":
    run()
