import streamlit as st
import streamlit.components.v1 as components

def run():
    st.title("🛡️ Consulta Nacional de SOAT (Fuente APESEG)")
    
    st.info("💡 APESEG es la base de datos central de Perú. Resuelve el captcha aquí abajo.")

    # URL oficial de consulta de APESEG
    url_apeseg = "https://www.apeseg.org.pe/consultas-soat/"
    
    # Intentamos cargar el portal oficial
    components.iframe(url_apeseg, height=800, scrolling=True)

    st.divider()
    st.caption("Si el recuadro no carga, es posible que debas usar la Opción B (App Móvil).")

if __name__ == "__main__":
    run()
