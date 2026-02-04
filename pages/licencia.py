import streamlit as st
import streamlit.components.v1 as components

def run():
    st.markdown("<h2 style='text-align: center;'>🪪 Consulta de Licencias de Conducir (MTC)</h2>", unsafe_allow_html=True)
    
    # Mensaje guía para el usuario sobre el captcha de imágenes
    st.warning("⚠️ Al marcar 'No soy un robot', es posible que se abra una ventana de selección de imágenes. Por favor, resuélvala dentro del recuadro.")

    # --- VISOR MTC CON RECORTE PERSONALIZADO ---
    # Ajustamos las medidas para centrar el formulario de Licencias
    html_mtc = """
    <div style="
        width: 100%; 
        height: 600px; 
        overflow: hidden; 
        border: 2px solid #B91C1C; 
        border-radius: 12px; 
        position: relative; 
        background: white;">
        
        <iframe src="https://licencias.mtc.gob.pe/#/index" 
            style="
                width: 1200px; 
                height: 1500px; 
                position: absolute; 
                top: -120px;       /* Recorte superior para quitar la barra roja de gob.pe */
                left: 50%; 
                margin-left: -600px; /* Centra el formulario de Documento de Identidad */
                border: none;"
            scrolling="no">
        </iframe>
    </div>
    """
    
    components.html(html_mtc, height=620)

    # --- ESPACIO PARA RESULTADOS ---
    if st.button("🚀 CAPTURAR DATOS DE LICENCIA", use_container_width=True):
        st.info("Una vez que el visor muestre los puntos y el récord del conductor, procesaremos la información aquí.")

if __name__ == "__main__":
    run()
