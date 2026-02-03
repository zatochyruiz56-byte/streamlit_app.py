import streamlit as st
import streamlit.components.v1 as components

def run():
    st.markdown("<h2 style='text-align: center; color: #1E3A8A;'>🔍 Central de Consultas SOAT</h2>", unsafe_allow_html=True)

    # --- CUADRO 1: APESEG (Historial y Vigencia) ---
    st.markdown("### 📊 1. Historial General")
    # Este es el código que ya te funcionaba perfectamente para APESEG
    html_apeseg = """
    <div style="width: 100%; height: 480px; overflow: hidden; border: 2px solid #1E3A8A; border-radius: 12px; position: relative; background: white;">
        <iframe src="https://www.apeseg.org.pe/consultas-soat/" 
            style="width: 1000px; height: 1200px; position: absolute; top: -560px; left: 60%; margin-left: -400px; border: none;"
            scrolling="no"></iframe>
    </div>
    """
    components.html(html_apeseg, height=500)

    st.markdown("---")

    # --- CUADRO 2: PACÍFICO (Descarga de PDF) ---
    st.markdown("### 📄 2. Descarga de Certificado")
    st.caption("Usa este cuadro para obtener el PDF si el vehículo es de Pacífico.")
    
    # IMPORTANTE: Usamos un proxy para que Pacífico no rechace la conexión
    html_pacifico = """
    <div style="width: 100%; height: 480px; overflow: hidden; border: 2px solid #0096d2; border-radius: 12px; position: relative; background: white;">
        <iframe src="https://api.allorigins.win/raw?url=https://www.pacifico.com.pe/consulta-soat" 
            style="width: 1000px; height: 1500px; position: absolute; top: -200px; left: 50%; margin-left: -500px; border: none;"
            scrolling="no"></iframe>
    </div>
    """
    components.html(html_pacifico, height=500)

    st.success("✅ Ambas fuentes están listas para consultar.")

if __name__ == "__main__":
    run()
