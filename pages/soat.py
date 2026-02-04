import streamlit as st
import streamlit.components.v1 as components

def run():
    st.markdown("<h2 style='text-align: center;'>🛡️ Consulta de Historial SOAT</h2>", unsafe_allow_html=True)

    # --- VISOR CON AJUSTE LATERAL CORREGIDO ---
    # Se aumenta el margin-left para esconder la parte izquierda sobrante
    html_apeseg = """
    <div style="
        width: 100%; 
        height: 500px; 
        overflow: hidden; 
        border: 2px solid #1E3A8A; 
        border-radius: 12px; 
        position: relative; 
        background: white;">
        
        <iframe src="https://www.apeseg.org.pe/consultas-soat/" 
            style="
                width: 1200px;      /* Ancho interno ampliado para maniobrar */
                height: 1500px; 
                position: absolute; 
                top: -560px;        /* Mantiene el recorte superior original */
                left: 50%;          /* Punto de anclaje centrado */
                margin-left: -615px; /* Empuja el contenido para limpiar la izquierda */
                border: none;"
            scrolling="no">
        </iframe>
    </div>
    """
    
    components.html(html_apeseg, height=520)

if __name__ == "__main__":
    run()
