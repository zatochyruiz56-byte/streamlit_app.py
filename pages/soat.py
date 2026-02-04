import streamlit as st
import streamlit.components.v1 as components

def run():
    st.markdown("<h2 style='text-align: center; color: #1E3A8A;'>🔍 Buscador SOAT Consolidado</h2>", unsafe_allow_html=True)

    # --- BLOQUE 1: APESEG (Tus coordenadas personalizadas) ---
    st.markdown("### 📊 1. Consulta de Historial")
    # Aplicando exactamente: top: -560px, left: 60%, margin-left: -400px
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

    # --- BLOQUE 2: INTERSEGURO (Vista para Descarga PDF) ---
    st.markdown("### 📄 2. Descarga de Certificado Digital")
    st.caption("Usa este panel para buscar el PDF si el SOAT es de Interseguro.")
    
    # Usamos el proxy para intentar evitar el bloqueo de "conexión rechazada"
    # Aquí no aplicamos recortes agresivos para que puedas ver todo el formulario
    html_interseguro = """
    <div style="width: 100%; height: 550px; overflow: hidden; border: 2px solid #00ac4e; border-radius: 12px; position: relative; background: white;">
        <iframe src="https://api.allorigins.win/raw?url=https://www.interseguro.pe/soat/consulta-soat" 
            style="
                width: 100%; 
                height: 100%; 
                border: none;"
            scrolling="yes">
        </iframe>
    </div>
    """
    components.html(html_interseguro, height=570)

if __name__ == "__main__":
    run()
