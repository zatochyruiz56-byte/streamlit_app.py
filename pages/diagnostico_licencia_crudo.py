import streamlit as st
import requests

def run():
    st.title("🚗 Consulta de Licencia de Conducir")
    
    # Endpoint extraído de tu captura de documentación
    API_URL = "https://seeker-v6.com/vehiculos/licencia_conductor"
    TOKEN = "sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"
    
    dni = st.text_input("Ingrese el número de DNI:", max_chars=8)
    
    if st.button("🔍 CONSULTAR LICENCIA"):
        if len(dni) == 8:
            # Encabezados estrictos según la documentación
            headers = {
                "Authorization": f"Bearer {TOKEN}",
                "Content-Type": "application/json"
            }
            
            # Payload con los dos parámetros requeridos: dni y tipo
            payload = {
                "dni": dni,
                "tipo": "dni" 
            }

            try:
                with st.spinner("Conectando con el servidor de transportes..."):
                    # Realizamos la petición POST
                    response = requests.post(API_URL, json=payload, headers=headers)
                
                # Verificamos si la respuesta es JSON antes de procesar
                try:
                    data = response.json()
                except:
                    # Si falla aquí, mostramos el error real del servidor (HTML)
                    st.error("❌ El servidor de licencias no está enviando una respuesta válida.")
                    st.warning(f"Código de estado: {response.status_code}")
                    with st.expander("Ver detalle técnico del error"):
                        st.code(response.text)
                    return

                if response.status_code == 200 and data.get("status") == "success":
                    st.success("Licencia encontrada con éxito")
                    st.json(data.get("data"))
                    
                    if "creditos_restantes" in data:
                        st.sidebar.metric("Créditos Disponibles", data["creditos_restantes"])
                else:
                    # Mostramos el mensaje de error que envíe la API
                    mensaje = data.get("message", "Error desconocido")
                    st.error(f"Error de la API: {mensaje}")

            except Exception as e:
                st.error(f"No se pudo establecer la conexión: {str(e)}")
        else:
            st.warning("El DNI debe tener 8 dígitos.")

if __name__ == "__main__":
    run()
