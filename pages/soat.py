import streamlit as st
import streamlit.components.v1 as components

def run():
    st.markdown("<h3 style='text-align: center; color: #1E3A8A;'>🛡️ Buscador SOAT</h3>", unsafe_allow_html=True)

    # --- AJUSTE QUIRÚRGICO DEL CORTE ---
    # margin-top: -400px -> Sube la página para esconder el logo y menú.
    # margin-left: -280px -> Mueve la página a la izquierda para centrar el cuadro.
    # transform: scale(1.1) -> Hace un pequeño zoom para que sea más fácil de tocar.
    
    recorte_perfecto = """
    <div style="
        width: 100%; 
        height: 280px; 
        overflow: hidden; 
        border: 2px solid #0047ab; 
        border-radius: 15px; 
        position: relative;
        background: white;">
        
        <iframe 
            src="https://www.apeseg.org.pe/consultas-soat/" 
            style="
                width: 1200px; 
                height: 1500px; 
                position: absolute; 
                top: -465px; 
                left: 50%; 
                margin-left: -600px; 
                border: none;
                transform: scale(1);
                transform-origin: 0 0;
            "
            scrolling="no">
        </iframe>
    </div>
    """

    components.html(recorte_perfecto, height=400)
    
    st.caption("🔍 Ingrese la placa y resuelva el captcha arriba.")

if __name__ == "__main__":
    run()
