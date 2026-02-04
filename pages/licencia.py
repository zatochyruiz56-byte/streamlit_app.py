import streamlit as st
import streamlit.components.v1 as components

def run():
    st.markdown("<h3 style='text-align: center;'>🪪 Consulta de Licencias de Conducir (MTC)</h3>", unsafe_allow_html=True)
    
    st.warning("⚠️ Resuelva el captcha de imágenes dentro del recuadro para ver los resultados.")

    # --- VISOR CON RECORTE AGRESIVO ---
    # Hemos subido el valor de 'top' de -280px a -550px para esconder todo lo superior
    html_mtc = """
    <div style="
        width: 100%; 
        height: 480px;      /* Reducimos la altura del visor para que no se asome lo de abajo */
        overflow: hidden; 
        border: 2px solid #B91C1C; 
        border-radius: 12px; 
        position: relative; 
        background: white;">
        
        <iframe src="https://licencias.mtc.gob.pe/#/index" 
            style="
                width: 1000px; 
                height: 2000px; 
                position: absolute; 
                top: -550px;       /* <--- ESTO SUBE EL FORMULARIO AL TOPE */
                left: 50%; 
                margin-left: -500px; /* Mantiene el formulario centrado */
                border: none;"
            scrolling="no">
        </iframe>
    </div>
    """
    
    components.html(html_mtc, height=520)

if __name__ == "__main__":
    run()
