import streamlit as st
import requests

def run():
    st.title("🚀 Consulta C4 Premiun")
    
    # Configuración de la API (Verifica que el endpoint sea el correcto)
    # Según tu captura, el endpoint premiun es consultapremiunc4
    API_URL = "https://seeker-v6.com/personas/api/consultapremiunc4"
    TOKEN = "sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"
    
    dni = st.text_input("Ingrese DNI", max_chars=8, placeholder="60799566")
    
    if st.button("🚀 REALIZAR CONSULTA"):
        if len(dni) == 8:
            # Headers más completos para evitar bloqueos
            headers = {
                "Authorization": f"Bearer {TOKEN}",
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
                "Referer": "https://seeker-v6.com/api/v1/documentation"
            }
            
            payload = {"dni": dni}

            try:
                with st.spinner("Conectando con el servidor..."):
                    response = requests.post(API_URL, json=payload, headers=headers, timeout=15)
                    data = response.json()

                if response.status_code == 200 and data.get("status") == "success":
                    st.success("Consulta finalizada con éxito")
                    st.json(data.get("data", {}))
                    
                    if "creditos_restantes" in data:
                        st.sidebar.metric("Créditos", data["creditos_restantes"])
                else:
                    # Manejo de error detallado
                    st.error("⚠️ Error en la respuesta del servidor")
                    with st.expander("Ver respuesta técnica"):
                        st.write(data)
                        
            except requests.exceptions.Timeout:
                st.error("⌛ La conexión tardó demasiado. Reintenta en unos momentos.")
            except Exception as e:
                st.error(f"❌ Error crítico: {str(e)}")
        else:
            st.warning("El DNI debe tener 8 dígitos.")

if __name__ == "__main__":
    run()
