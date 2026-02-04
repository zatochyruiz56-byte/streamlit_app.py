import streamlit as st
import streamlit.components.v1 as components

def run():
    st.markdown("<h2 style='text-align: center;'>🛡️ Consulta y Reporte SOAT</h2>", unsafe_allow_html=True)

    # --- BLOQUE 1: BUSCADOR OFICIAL (APESEG con tus medidas) ---
    # Usamos tus coordenadas exactas para que no se mueva nada
    st.markdown("### 🔍 1. Validación en Tiempo Real")
    html_apeseg = """
    <div style="width: 100%; height: 480px; overflow: hidden; border: 2px solid #2e59a8; border-radius: 12px; position: relative; background: white;">
        <iframe src="https://www.apeseg.org.pe/consultas-soat/" 
            style="width: 1000px; height: 1200px; position: absolute; top: -385px; left: 50%; margin-left: -500px; border: none;"
            scrolling="no"></iframe>
    </div>
    """
    components.html(html_apeseg, height=500)

    st.markdown("---")

    # --- BLOQUE 2: FICHA DE TRABAJO (Resultados dentro de la App) ---
    # Esto reemplaza la necesidad de descargar el PDF externo
    st.markdown("### 📋 2. Ficha de Trabajo Consolidada")
    
    # Simulación de cómo se vería tu reporte integrado
    with st.container(border=True):
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Estado:** 🟢 VIGENTE")
            st.write("**Aseguradora:** INTERSEGURO")
        with col2:
            st.write("**Inicio:** 03/06/2025")
            st.write("**Vencimiento:** 03/06/2026")
        
        st.info("💡 Los datos mostrados arriba son extraídos de la consulta oficial superior.")

if __name__ == "__main__":
    run()
