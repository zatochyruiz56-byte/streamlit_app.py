import streamlit as st
import streamlit.components.v1 as components

def run():
    st.markdown("<h3 style='text-align: center;'>🔍 Buscador Oficial SOAT</h3>", unsafe_allow_html=True)

    # --- AJUSTE DE PRECISIÓN ---
    # He bajado el valor de 'top' para que el formulario no quede escondido arriba.
    # He aumentado el 'height' para que el botón 'Consultar' también sea visible.
    
    recorte_ajustado = """
    <div style="
        width: 100%; 
        height: 520px; 
        overflow: hidden; 
        border: 2px solid #1E3A8A; 
        border-radius: 10px; 
        position: relative;
        background: white;">
        
        <iframe 
            src="https://www.apeseg.org.pe/consultas-soat/" 
            style="
                width: 1000px; 
                height: 1500px; 
                position: absolute; 
                top: -360px; /* Antes estaba en -465, lo subí para que veas la placa */
                left: 50%; 
                margin-left: -500px; 
                border: none;
            "
            scrolling="no">
        </iframe>
    </div>
    """

    components.html(recorte_ajustado, height=530)
    
    st.info("👆 Ingresa la placa en el recuadro blanco de arriba y resuelve el captcha.")

if __name__ == "__main__":
    run()
