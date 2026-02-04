import streamlit as st
import streamlit.components.v1 as components

def run():
    st.markdown("<h2 style='text-align: center;'>🛡️ Consulta de Historial SOAT</h2>", unsafe_allow_html=True)

    # --- BOTÓN DE REINICIO ---
    # Este botón refresca la sección para volver a buscar
    if st.button("🔄 Realizar otra búsqueda", use_container_width=True):
        st.rerun()

    # --- VISOR APESEG (Tus medidas originales) ---
    # top: -560px, left: 60%, margin-left: -400px
    html_apeseg = """
    <div style="width: 100%; height: 500px; overflow: hidden; border: 2px solid #1E3A8A; border-radius: 12px; position: relative; background: white;">
        <iframe src="https://www.apeseg.org.pe/consultas-soat/" 
            style="
                width: 1000px; 
                height: 1500px; 
                position: absolute; 
                top: -560px; 
                left: 60%; 
                margin-left: -400px; 
                border: none;"
            scrolling="no">
        </iframe>
    </div>
    """
    
    components.html(html_apeseg, height=520)
    
    st.caption("Resuelve el captcha y presiona 'Consultar'. Usa el botón superior para limpiar los datos.")

if __name__ == "__main__":
    run()
