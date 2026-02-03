import streamlit as st
import requests

def run():
    st.title("📄 Consulta C4 Premium")
    
    API_URL = "https://seeker-v6.com/personas/api/consultapremiunc4"
    TOKEN = "sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"
    
    dni = st.text_input("Ingrese DNI de 8 dígitos:", max_chars=8)
    
    if st.button("🚀 REALIZAR CONSULTA"):
        if len(dni) == 8:
            headers = {
                "Authorization": f"Bearer {TOKEN}",
                "Content-Type": "application/json"
            }
            payload = {"dni": dni}

            try:
                with st.spinner("Consultando con RENIEC..."):
                    response = requests.post(API_URL, json=payload, headers=headers)
                    data = response.json()

                if response.status_code == 200:
                    if data.get("status") == "success":
                        st.success("¡Datos encontrados!")
                        st.json(data.get("data"))
                    else:
                        # Error específico del proveedor (lo que te pasa ahora)
                        st.error(f"⚠️ Servidor dice: {data.get('message')}")
                        st.info("Esto suele ser un problema temporal de RENIEC. Intenta en unos minutos.")
                else:
                    st.error(f"Error de API: {response.status_code}")
                
                # Mostrar siempre los créditos si vienen en la respuesta
                if "creditos_restantes" in data:
                    st.sidebar.metric("Créditos Restantes", data["creditos_restantes"])

            except Exception as e:
                st.error("Error de conexión local. Revisa tu internet.")
        else:
            st.warning("Escriba un DNI válido.")

if __name__ == "__main__":
    run()
