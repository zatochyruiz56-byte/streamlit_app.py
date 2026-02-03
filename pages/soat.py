import streamlit as st
import webbrowser

def run():
    st.markdown("<h2 style='text-align: center; color: #1E3A8A;'>🛡️ Central de Consultas SOAT</h2>", unsafe_allow_html=True)
    
    with st.container(border=True):
        placa = st.text_input("Ingrese la Placa del Vehículo", max_chars=6, placeholder="ABC123").upper()
        
        st.markdown("---")
        st.write("Seleccione la fuente de consulta:")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Opción 1: APESEG para historial y vigencia general
            st.info("**APESEG**\n\nIdeal para ver historial y vigencia de todas las aseguradoras.")
            if st.button("📊 Consultar Historial", use_container_width=True):
                if placa:
                    st.link_button("Abrir APESEG Oficial", "https://www.apeseg.org.pe/consultas-soat/")
                else:
                    st.warning("Por favor, ingrese una placa.")

        with col2:
            # Opción 2: Pacífico para descarga de PDF
            st.success("**PACÍFICO**\n\nUsa esta opción si necesitas descargar el certificado en PDF.")
            if st.button("📄 Descargar PDF (SOAT)", use_container_width=True):
                if placa:
                    # Intentamos enviar la placa directamente en la URL si el sitio lo permite
                    st.link_button("Abrir Pacífico Seguros", "https://www.pacifico.com.pe/consulta-soat")
                else:
                    st.warning("Por favor, ingrese una placa.")

    # --- PLANTILLA DE RESULTADOS (Para llenado manual o visual) ---
    if placa:
        st.markdown(f"### 📋 Ficha de Trabajo: {placa}")
        with st.expander("Ver Formato de Reporte Personalizado", expanded=True):
            st.markdown(f"""
            | Concepto | Detalle |
            | :--- | :--- |
            | **Vehículo** | {placa} |
            | **Aseguradora** | *(Consultar en links arriba)* |
            | **Estado** | VIGENTE / VENCIDO |
            """)
            st.caption("Una vez consultes en las webs oficiales, puedes validar los datos aquí.")

if __name__ == "__main__":
    run()
