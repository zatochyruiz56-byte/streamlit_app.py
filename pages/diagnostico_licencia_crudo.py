import streamlit as st
import requests

def run():
    st.title("🚗 Consulta de Licencia de Conducir")
    st.info("Esta consulta utiliza el endpoint de vehículos para verificar licencias.")

    # Configuración según la nueva documentación
    API_URL = "https://seeker-v6.com/vehiculos/licencia_conductor"
    TOKEN = "sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"
    
    dni = st.text_input("Ingrese DNI (8 dígitos)", max_chars=8)
    
    if st.button("🔍 CONSULTAR LICENCIA"):
        if len(dni) == 8:
            headers = {
                "Authorization": f"Bearer {TOKEN}",
                "Content-Type": "application/json"
            }
            # Según la documentación, requiere 'dni' y 'tipo'
            payload = {
                "dni": dni,
                "tipo": "dni" 
            }

            try:
                with st.spinner("Buscando en el registro de conductores..."):
                    response = requests.post(API_URL, json=payload, headers=headers)
                    data = response.json()

                if response.status_code == 200:
                    if data.get("status") == "success":
                        st.success("Licencia encontrada")
                        st.json(data.get("data"))
                    else:
                        st.error(f"Mensaje de la API: {data.get('message')}")
                else:
                    st.error(f"Error técnico (HTTP {response.status_code})")
                
                # Inspección técnica para ver el error exacto
                with st.expander("Ver respuesta técnica detallada"):
                    st.write(data)

            except Exception as e:
                st.error(f"Error de conexión: {str(e)}")
        else:
            st.warning("Por favor, ingrese un DNI válido.")

if __name__ == "__main__":
    run()
