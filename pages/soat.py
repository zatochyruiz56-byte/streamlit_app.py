import streamlit as st
import streamlit.components.v1 as components

def run():
    st.markdown("<h2 style='text-align: center; color: #1E3A8A;'>🛡️ Central SOAT Multi-Consulta</h2>", unsafe_allow_html=True)

    # --- BLOQUE 1: APESEG (Tus coordenadas exactas que sí funcionan) ---
    st.markdown("### 📊 1. Historial General")
    html_apeseg = """
    <div style="width: 100%; height: 500px; overflow: hidden; border: 2px solid #1E3A8A; border-radius: 12px; position: relative; background: white;">
        <iframe src="https://www.apeseg.org.pe/consultas-soat/" 
            style="width: 1000px; height: 1500px; position: absolute; top: -560px; left: 60%; margin-left: -400px; border: none;"
            scrolling="no"></iframe>
    </div>
    """
    components.html(html_apeseg, height=520)

    st.markdown("---")

    # --- BLOQUE 2: INTERSEGURO (Versión optimizada para evitar error de dominio) ---
    st.markdown("### 📄 2. Descarga de Certificado (Interseguro)")
    
    # Usamos la URL de consulta directa para intentar evadir el bloqueo del reCAPTCHA de dominio
    html_interseguro = """
    <div style="width: 100%; height: 550px; overflow: hidden; border: 2px solid #00ac4e; border-radius: 12px; position: relative; background: white;">
        <iframe src="https://www.interseguro.pe/soat/consulta-soat" 
            style="width: 100%; height: 1500px; position: absolute; top: -280px; left: 50%; margin-left: -500px; border: none;"
            scrolling="no"></iframe>
    </div>
    """
    components.html(html_interseguro, height=570)

if __name__ == "__main__":
    run()
