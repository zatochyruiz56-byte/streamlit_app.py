import streamlit as st
import streamlit.components.v1 as components

def run():
    st.markdown("<h2 style='text-align: center;'>🛡️ Consulta de Historial SOAT</h2>", unsafe_allow_html=True)

    # --- VISOR CON RECORTE LATERAL QUIRÚRGICO ---
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
                width: 1600px; /* Aumentamos el ancho interno para tener más margen de maniobra */
                height: 3000px; 
                position: absolute; 
                top: -600px;    /* Ajuste superior basado en tu código anterior */
                left: 50%;      /* Centramos el punto de anclaje */
                margin-left: -600px; /* Empujamos 800px a la izquierda para esconder el borde izquierdo real */
                border: none;"
                transform: scale(2.0); /* <--- AQUÍ HACES EL ZOOM */
        transform-origin: top center; /* <--- ESTO MANTIENE EL ZOOM CENTRADO */
    "
            scrolling="no">
        </iframe>
    </div>
    """
    
    components.html(html_apeseg, height=520)

if __name__ == "__main__":
    run()
