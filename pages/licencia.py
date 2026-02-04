import streamlit as st
import requests

def run():
    st.set_page_config(page_title="MTC Factiliza Pro", page_icon="💳")
    
    st.markdown("<h2 style='text-align: center;'>🪪 Consulta MTC via Factiliza</h2>", unsafe_allow_html=True)
    
    # Configuración de credenciales
    TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI0MDMwNSIsImh0dHA6Ly9zY2hlbWFzLm1pY3Jvc29mdC5jb20vd3MvMjAwOC8wNi9pZGVudGl0eS9jbGFpbXMvcm9sZSI6ImNvbnN1bHRvciJ9.Gsokm2AIDVCMdG5etymgkljwqXoCrb7b24c75H_VMr0"
    headers = {"Authorization": f"Bearer {TOKEN}"}

    dni = st.text_input("Ingrese DNI del conductor:", max_chars=8, placeholder="Ej. 44747700")

    if st.button("🚀 Consultar Licencia", use_container_width=True):
        if len(dni) == 8 and dni.isdigit():
            with st.spinner("Buscando en Factiliza..."):
                try:
                    # Construcción de la URL dinámica
                    url = f"https://api.factiliza.com/v1/licencia/info/{dni}"
                    
                    response = requests.get(url, headers=headers)
                    
                    if response.status_code == 200:
                        data = response.json()
                        
                        # Mostramos los datos de manera elegante
                        st.balloons()
                        st.success("✅ Información recuperada con éxito")
                        
                        # Estructura basada en respuesta típica de licencias
                        with st.expander("📄 Ver Ficha Completa", expanded=True):
                            col1, col2 = st.columns(2)
                            with col1:
                                st.write(f"**Nombre Completo:** {data.get('nombre', 'No disponible')}")
                                st.write(f"**Clase/Categoría:** {data.get('categoria', 'N/A')}")
                            with col2:
                                st.write(f"**Nro. Licencia:** {data.get('numeroLicencia', dni)}")
                                st.write(f"**Fecha Vencimiento:** {data.get('fechaVencimiento', 'N/A')}")
                            
                            st.divider()
                            st.subheader("📊 Récord del Conductor")
                            st.metric("Puntos Acumulados", data.get("puntos", "0"))
                            st.write(f"**Estado:** {data.get('estado', 'VIGENTE')}")
                    
                    elif response.status_code == 401:
                        st.error("🚫 Error de Autorización: Tu token ha expirado o es incorrecto.")
                    else:
                        st.error(f"⚠️ Error {response.status_code}: No se pudo obtener la información.")
                        
                except Exception as e:
                    st.error(f"❌ Error de conexión: {str(e)}")
        else:
            st.warning("⚠️ Por favor, ingrese un DNI válido de 8 dígitos numéricos.")

if __name__ == "__main__":
    run()
