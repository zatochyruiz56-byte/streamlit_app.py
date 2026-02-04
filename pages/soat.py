import streamlit as st
import streamlit.components.v1 as components

def run():
    st.markdown("<h2 style='text-align: center;'>🛡️ Consulta de Historial SOAT</h2>", unsafe_allow_html=True)

    # --- VISOR CON RECORTE LATERAL QUIRÚRGICO ---
    # Usamos -615px para empujar el contenido y eliminar lo que se ve a la izquierda
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
                width: 1300px;      /* Aumentamos un poco el ancho interno para dar margen */
                height: 1500px; 
                position: absolute; 
                top: -560px;        /* Mantiene el recorte superior que ya te funcionaba */
                left: 50%; 
                margin-left: -300px; /* <--- ESTA ES LA MEDIDA PARA ELIMINAR LA IZQUIERDA */
                border: none;"
            scrolling="no">
        </iframe>
    </div>
    """
    
    components.html(html_apeseg, height=520)

if __name__ == "__main__":
    run()
