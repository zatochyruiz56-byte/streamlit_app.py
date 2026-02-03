import streamlit as st
import streamlit.components.v1 as components

def run():
    st.markdown("<h2 style='text-align: center; color: #1E3A8A;'>🛡️ Consulta SOAT Directa</h2>", unsafe_allow_html=True)
    st.info("Escribe la placa y resuelve el captcha abajo para ver el resultado oficial.")

    # Contenedor que recorta la página oficial para mostrar solo el formulario
    # Ajustado según tus capturas para centrar el 'Número de Placa'
    recorte_html = """
    <div style="
        width: 100%; 
        height: 480px; 
        overflow: hidden; 
        border: 2px solid #2e59a8; 
        border-radius: 12px; 
        position: relative;
        background: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
        
        <iframe 
            src="https://www.apeseg.org.pe/consultas-soat/" 
            style="
                width: 1000px; 
                height: 1200px; 
                position: absolute; 
                top: -500px; /* Sube la web para ocultar el encabezado azul */
                left: 50%; 
                margin-left: -370px; /* Centra el contenido horizontalmente */
                border: none;
            "
            scrolling="no">
        </iframe>
    </div>
    """

    # Renderizamos el componente
    components.html(recorte_html, height=500)

    st.warning("⚠️ Una vez des clic en 'Consultar', el resultado aparecerá en el cuadro blanco.")

if __name__ == "__main__":
    run()
