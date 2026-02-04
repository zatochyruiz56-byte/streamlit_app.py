import streamlit as st
import streamlit.components.v1 as components

def run():
    # Título de la sección
    st.markdown("<h2 style='text-align: center;'>🛡️ Consulta de Historial SOAT</h2>", unsafe_allow_html=True)

    # --- VISOR APESEG (Tus medidas originales) ---
    # Se eliminaron todos los botones adicionales para dejar solo la fuente oficial
    html_apeseg = """
    <div style="width: 100%; height: 500px; overflow: hidden; border: 2px solid #1E3A8A; border-radius: 12px; position: relative; background: white;">
        <iframe src="https://www.apeseg.org.pe/consultas-soat/" 
            style="
                width: 1000px; 
                height: 1500px; 
                position: absolute; 
                top: -560px; 
                left: 70%; 
                margin-left: -420px; 
                border: none;"
            scrolling="no">
        </iframe>
    </div>
    """
    
    # Renderizado del componente
    components.html(html_apeseg, height=520)

if __name__ == "__main__":
    run()
