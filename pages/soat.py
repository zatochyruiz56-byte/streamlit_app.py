import streamlit as st
import streamlit.components.v1 as components

def run():
    st.markdown("<h2 style='text-align: center; color: #1E3A8A;'>🔍 Central SOAT Multi-Consulta</h2>", unsafe_allow_html=True)

    # --- BLOQUE 1: APESEG (Tus medidas exactas) ---
    st.markdown("### 📊 1. Vista Recortada (APESEG)")
    html_apeseg = """
    <div style="width: 100%; height: 500px; overflow: hidden; border: 2px solid #1E3A8A; border-radius: 12px; position: relative; background: white;">
        <iframe src="https://www.apeseg.org.pe/consultas-soat/" 
            style="
                width: 1000px; 
                height: 1500px; 
                position: absolute; 
                top: -560px; 
                left: 60%; 
                margin-left: -400px; 
                border: none;"
            scrolling="no">
        </iframe>
    </div>
    """
    components.html(html_apeseg, height=520)

    st.markdown("---")

    # --- BLOQUE 2: INTERSEGURO (Vista Completa para PDF) ---
    st.markdown("### 📄 2. Vista Completa (Interseguro)")
    st.caption("En este cuadro puedes ver toda la página para buscar y descargar el SOAT electrónico.")
    
    # Aquí no aplicamos recortes (top: 0) para que veas toda la página
    html_completo = """
    <div style="width: 100%; height: 600px; border: 2px solid #00ac4e; border-radius: 12px; overflow: hidden; background: white;">
        <iframe src="https://www.interseguro.pe/soat/consulta-soat" 
            style="width: 100%; height: 100%; border: none;"
            scrolling="yes">
        </iframe>
    </div>
    """
    components.html(html_completo, height=620)

if __name__ == "__main__":
    run()
