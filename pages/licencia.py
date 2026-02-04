import streamlit as st
import requests

def run():
    st.set_page_config(page_title="MTC Factiliza Full Data", layout="wide")
    
    st.markdown("<h2 style='text-align: center;'>🪪 Reporte Integral de Licencia (Factiliza)</h2>", unsafe_allow_html=True)
    
    TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI0MDMwNSIsImh0dHA6Ly9zY2hlbWFzLm1pY3Jvc29mdC5jb20vd3MvMjAwOC8wNi9pZGVudGl0eS9jbGFpbXMvcm9sZSI6ImNvbnN1bHRvciJ9.Gsokm2AIDVCMdG5etymgkljwqXoCrb7b24c75H_VMr0"
    headers = {"Authorization": f"Bearer {TOKEN}"}

    dni = st.text_input("Ingrese DNI:", max_chars=8)

    if st.button("🚀 Consultar Información Completa", use_container_width=True):
        if len(dni) == 8:
            with st.spinner("Extrayendo historial completo..."):
                url = f"https://api.factiliza.com/v1/licencia/info/{dni}"
                response = requests.get(url, headers=headers)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # --- SECCIÓN 1: DATOS PERSONALES ---
                    st.subheader("👤 Datos del Conductor")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.write(f"**Nombre:** {data.get('nombre', '---')}")
                    with col2:
                        st.write(f"**DNI:** {dni}")
                    with col3:
                        st.metric("Puntos", data.get("puntos", "0"))

                    st.divider()

                    # --- SECCIÓN 2: DETALLE DE LICENCIA ---
                    st.subheader("💳 Información de la Licencia")
                    c1, c2, c3 = st.columns(3)
                    with c1:
                        st.info(f"**Categoría:** {data.get('categoria', 'N/A')}")
                    with c2:
                        st.info(f"**Nro. Licencia:** {data.get('numeroLicencia', 'N/A')}")
                    with c3:
                        st.info(f"**Vencimiento:** {data.get('fechaVencimiento', 'N/A')}")

                    # --- SECCIÓN 3: RESTRICCIONES Y ESTADO ---
                    st.subheader("⚠️ Restricciones y Observaciones")
                    st.warning(data.get("restricciones", "Sin restricciones registradas"))
                    
                    # --- SECCIÓN 4: DATA CRUDA (JSON) ---
                    # Esto te permite ver si hay campos extra que no pusimos en las columnas
                    with st.expander("📦 Ver JSON Técnico (Toda la info)", expanded=False):
                        st.json(data)
                else:
                    st.error(f"Error {response.status_code}: No se pudo conectar con la API.")
        else:
            st.warning("Ingrese un DNI de 8 dígitos.")

if __name__ == "__main__":
    run()
