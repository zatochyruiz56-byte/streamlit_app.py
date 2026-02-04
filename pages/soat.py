import streamlit as st
import streamlit.components.v1 as components

def run():
    st.markdown("<h2 style='text-align: center;'>🛡️ Consulta de Historial SOAT</h2>", unsafe_allow_html=True)

    # --- 1. VISOR ORIGINAL (Medidas exactas: top: -560px, left: 60%) ---
    # Al recargar la página, este iframe vuelve siempre al inicio
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

    # --- 2. BOTÓN DE REINICIO TOTAL ---
    # Se ha eliminado el botón de 'Pasar a Plantilla' por tu requerimiento
    if st.button("🔄 Realizar otra búsqueda", use_container_width=True):
        # Limpiamos todo el estado de la sesión para asegurar que no haya bloqueos
        for key in st.session_state.keys():
            del st.session_state[key]
        # Forzamos el reinicio de la aplicación hacia la página original
        st.rerun()

    st.caption("Resuelva el captcha arriba para ver los resultados oficiales.")

if __name__ == "__main__":
    run()
