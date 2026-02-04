import streamlit as st
import requests

def run():
    st.set_page_config(page_title="Consulta MTC Pro", page_icon="🪪")
    
    st.markdown("<h2 style='text-align: center;'>🚀 Consulta de Licencias MTC (Automática)</h2>", unsafe_allow_html=True)
    
    # Configuración de la API
    API_URL = "https://api.consultasperu.com/api/v1/query/license"
    TOKEN = "be8b5bbe5b741ace308b5dba137d78c8c6a71c1217a8dad1db5db816883cc863"

    dni = st.text_input("Ingrese el número de DNI:", max_chars=8)

    if st.button("🔍 Consultar Ahora", use_container_width=True):
        if len(dni) == 8:
            with st.spinner("Conectando con la base de datos del MTC..."):
                try:
                    # Estructura del Body según documentación
                    payload = {
                        "token": TOKEN,
                        "dni": dni
                    }
                    headers = {'Content-Type': 'application/json'}
                    
                    response = requests.post(API_URL, json=payload, headers=headers)
                    
                    if response.status_code == 200:
                        resultado = response.json()
                        
                        if resultado.get("success"):
                            data = resultado["data"] #
                            
                            # Mostrar Resultados en tarjetas limpias
                            st.success(f"✅ Conductor: {data['full_name']}")
                            
                            col1, col2, col3 = st.columns(3)
                            # Accediendo a la lista de licencias
                            licencia = data["license"][0] 
                            
                            with col1:
                                st.metric("Categoría", licencia["category"])
                            with col2:
                                st.metric("Estado", licencia["status"])
                            with col3:
                                st.metric("Vence", licencia["date_of_due"])
                                
                            st.info(f"📝 Observaciones: {licencia['observations']}")
                        else:
                            st.error(f"❌ Error: {resultado.get('message', 'No se encontraron datos')}")
                    else:
                        st.error(f"⚠️ Error de conexión (Código: {response.status_code})")
                        
                except Exception as e:
                    st.error(f"🔥 Ocurrió un error inesperado: {e}")
        else:
            st.warning("Please ingrese un DNI válido de 8 dígitos.")

if __name__ == "__main__":
    run()
