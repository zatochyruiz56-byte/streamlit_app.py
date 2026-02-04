import streamlit as st
import streamlit.components.v1 as components

def run():
    st.markdown("<h2 style='text-align: center;'>🪪 Consulta de Licencias de Conducir (MTC)</h2>", unsafe_allow_html=True)
    
    st.warning("⚠️ Al marcar 'No soy un robot', resuelva el captcha de imágenes dentro del recuadro.")

    # --- VISOR CON RECORTE SUPERIOR AJUSTADO ---
    html_mtc = """
    <div style="
        width: 100%; 
        height: 550px; 
        overflow: hidden; 
        border: 2px solid #B91C1C; 
        border-radius: 12px; 
        position: relative; 
        background: white;">
        
        <iframe src="https://licencias.mtc.gob.pe/#/index" 
            style="
                width: 1000px; 
                height: 1500px; 
                position: absolute; 
                top: -240px;       /* SUBIMOS MÁS EL CONTENIDO (Antes -120px) */
                left: 50%; 
                margin-left: -500px; /* Centra el formulario de DNI */
                border: none;"
            scrolling="no">
        </iframe>
    </div>
    """
    
    components.html(html_mtc, height=570)

if __name__ == "__main__":
    run()
