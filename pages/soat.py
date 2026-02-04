import streamlit as st
import streamlit.components.v1 as components

def run():
    st.markdown("<h2 style='text-align: center; color: #1E3A8A;'>🛡️ Central de Consultas SOAT</h2>", unsafe_allow_html=True)

    # --- BLOQUE 1: APESEG (Tus medidas exactas) ---
    st.markdown("### 📊 1. Historial y Vigencia (APESEG)")
    # Usamos tus coordenadas: top: -560px, left: 60%, margin-left: -400px
    html_apeseg = """
    <div style="width: 100%; height: 500px; overflow: hidden; border: 2px solid #1E3A8A; border-radius: 12px; position: relative; background: white;">
        <iframe src="https://www.apeseg.org.pe/consultas-soat/" 
            style="width: 1000px; height: 1500px; position: absolute; top: -560px; left: 60%; margin-left: -400px; border: none;"
            scrolling="no"></iframe>
    </div>
    """
    components.html(html_apeseg, height=520)

    st.markdown("---")

    # --- BLOQUE 2: INTERSEGURO/PACÍFICO (Desbloqueado para PDF) ---
    st.markdown("### 📄 2. Descarga de Certificado Electrónico")
    st.caption("Este cuadro usa un puente de conexión para evitar el bloqueo de seguridad.")
    
    # Usamos 'allorigins' para "limpiar" el bloqueo de la cara triste
    # Cambiamos el top para que veas el formulario de Interseguro de una vez
    html_desbloqueado = """
    <div style="width: 100%; height: 550px; overflow: hidden; border: 2px solid #00ac4e; border-radius: 12px; position: relative; background: white;">
        <iframe src="https://api.allorigins.win/raw?url=https://www.interseguro.pe/soat/consulta-soat" 
            style="width: 100%; height: 1500px; position: absolute; top: -320px; left: 50%; margin-left: -500px; border: none;"
            scrolling="no"></iframe>
    </div>
    """
    components.html(html_desbloqueado, height=570)

if __name__ == "__main__":
    run()
