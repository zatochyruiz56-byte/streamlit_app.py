import streamlit as st
import streamlit.components.v1 as components

def run():
    st.markdown("<h3 style='text-align: center;'>🪪 Consulta de Licencias de Conducir (MTC)</h3>", unsafe_allow_html=True)
    
    st.warning("⚠️ Resuelva el captcha 'No soy un robot' dentro del recuadro.")

    # --- VISOR CON CORTE PARA QUEDAR EN EL FORMULARIO ---
    # Usamos -520px para saltar la cabecera y centrar el cuadro de DNI
    html_mtc = """
    <div style="
        width: 100%; 
        height: 480px;      /* Altura ajustada para no mostrar servicios inferiores */
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
                top: -520px;       /* <--- SUBE HASTA EL TÍTULO 'CONSULTA DE LICENCIAS' */
                left: 50%; 
                margin-left: -500px; /* Centra el formulario horizontalmente */
                border: none;"
            scrolling="no">
        </iframe>
    </div>
    """
    
    components.html(html_mtc, height=500)

if __name__ == "__main__":
    run()
