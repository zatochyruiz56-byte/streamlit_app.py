import streamlit as st
import requests

def run():
    st.title("Consulta C4 - RENIEC")
    st.write("Ingrese el DNI para obtener la información completa.")

    # Configuración de la API
    API_URL = "https://seeker-v6.com/personas/api/consultapremiunc4"
    TOKEN = "sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"
    
    # Formulario de búsqueda
    with st.form("c4_form"):
        dni = st.text_input("DNI (8 dígitos)", max_chars=8)
        submitted = st.form_submit_button("Consultar")

    if submitted:
        if len(dni) == 8 and dni.isdigit():
            headers = {
                "Authorization": f"Bearer {TOKEN}",
                "Content-Type": "application/json"
            }
            payload = {"dni": dni}

            try:
                with st.spinner("Consultando datos..."):
                    response = requests.post(API_URL, json=payload, headers=headers)
                    data = response.json()

                if response.status_code == 200 and data.get("status") == "success":
                    st.success("Consulta exitosa")
                    
                    # Mostrar resultados (ajusta según los campos reales de 'data')
                    st.json(data.get("data", {}))
                    
                    st.info(f"Créditos restantes: {data.get('creditos_restantes')}")
                else:
                    st.error(f"Error: {data.get('message', 'No se pudo completar la consulta')}")
            
            except Exception as e:
                st.error(f"Ocurrió un error de conexión: {e}")
        else:
            st.warning("Por favor, ingrese un DNI válido de 8 dígitos.")

if __name__ == "__main__":
    run()
