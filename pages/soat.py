import streamlit as st
import streamlit.components.v1 as components

def run():
    st.markdown("<h2 style='text-align: center;'>🛡️ Consulta de Historial SOAT</h2>", unsafe_allow_html=True)

    # --- VISOR CON ZOOM Y RECORTE DE COSTADOS ---
    html_apeseg = """
    <div style="
        width: 100%; 
        height: 520px; 
        overflow: hidden; 
        border: 2px solid #1E3A8A; 
        border-radius: 12px; 
        position: relative; 
        background: white;">
        
        <iframe src="https://www.apeseg.org.pe/consultas-soat/" 
            style="
                width: 1600px; 
                height: 3000px; 
                position: absolute; 
                top: -720px;       /* Ajustado para compensar el zoom */
                left: 80%; 
                margin-left: -1040px; /* Empujado más a la izquierda para borrar el anuncio */
                border: none;
                transform: scale(1.3); /* Zoom al 130% para llenar la pantalla */
                transform-origin: top left;
            "
            scrolling="no">
        </iframe>
    </div>
    """
    
    components.html(html_apeseg, height=540)

if __name__ == "__main__":
    run()
