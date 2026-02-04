import streamlit as st
import streamlit.components.v1 as components

def run():
    st.markdown("<h2 style='text-align: center;'>🛡️ Consulta de Historial SOAT</h2>", unsafe_allow_html=True)

    # --- VISOR APESEG (Ajuste de margen izquierdo) ---
    # He cambiado left a 50% y aumentado el margin-left negativo para recortar la izquierda.
    html_apeseg = """
    <div style="width: 100%; height: 500px; overflow: hidden; border: 2px solid #1E3A8A; border-radius: 12px; position: relative; background: white;">
        <iframe src="https://www.apeseg.org.pe/consultas-soat/" 
            style="
                width: 1500px; 
                height: 3000px; 
                position: absolute; 
                top: -560px; /* Mantenemos tu recorte superior */
                left: 10%;    /* Bajamos de 60% a 45% para moverlo a la izquierda */
                margin-left: -200px; /* Ajuste para centrar el formulario tras el recorte */
                border: none;"
            scrolling="no">
        </iframe>
    </div>
    """
    
    components.html(html_apeseg, height=520)

if __name__ == "__main__":
    run()
