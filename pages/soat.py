import streamlit as st
import streamlit.components.v1 as components

def run():
    st.markdown("<h2 style='text-align: center; color: #1E3A8A;'>🛡️ Consulta de SOAT Nacional</h2>", unsafe_allow_html=True)
    
    st.info("💡 Ingresa la placa y resuelve el captcha para ver la vigencia e historial completo.")

    # --- CONTENEDOR ESPEJO (SOLO APESEG) ---
    # Ajustado quirúrgicamente para centrar el formulario
    recorte_html = """
    <div style="
        width: 100%; 
        height: 520px; 
        overflow: hidden; 
        border: 2px solid #1E3A8A; 
        border-radius: 12px; 
        position: relative;
        background: white;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
        
        <iframe 
            src="https://www.apeseg.org.pe/consultas-soat/" 
            style="
                width: 1000px; 
                height: 1200px; 
                position: absolute; 
                top: -560px; /* Oculta el encabezado oficial */
                left: 60%; 
                margin-left: -400px; /* Centra el contenido horizontalmente */
                border: none;
            "
            scrolling="no">
        </iframe>
    </div>
    """

    # Renderizamos el espejo
    components.html(recorte_html, height=540)

    # --- RECORDATORIO PARA EL USUARIO ---
    st.warning("⚠️ Una vez des clic en 'Consultar', el resultado aparecerá arriba. Desplázate dentro del cuadro para ver el historial.")

if __name__ == "__main__":
    run()
