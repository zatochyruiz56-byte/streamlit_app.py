import streamlit as st
import streamlit.components.v1 as components

def run():
    st.markdown("<h2 style='text-align: center;'>🛡️ Consulta de Historial SOAT</h2>", unsafe_allow_html=True)

    # --- VISOR ORIGINAL (Restaurado a tus medidas previas) ---
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
                width: 1000px; 
                height: 1500px; 
                position: absolute; 
                top: -560px;       /* Oculta el encabezado oficial */
                left: 60%; 
                margin-left: -400px; /* Centra el contenido horizontalmente */
                border: none;"
            scrolling="no">
        </iframe>
    </div>
    """
    
    components.html(html_apeseg, height=520)

if __name__ == "__main__":
    run()
