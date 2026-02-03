import streamlit as st
import streamlit.components.v1 as components

def run():
    st.markdown("<h2 style='text-align: center; color: #1E3A8A;'>🔍 Buscador Dual SOAT</h2>", unsafe_allow_html=True)

    # --- BLOQUE 1: APESEG (Historial y Vigencia) ---
    st.markdown("#### 📊 1. Consulta General (APESEG)")
    # El recorte de APESEG que ya te funcionaba bien
    html_apeseg = """
    <div style="width: 100%; height: 460px; overflow: hidden; border: 2px solid #2e59a8; border-radius: 12px; position: relative; background: white;">
        <iframe src="https://www.apeseg.org.pe/consultas-soat/" 
            style="width: 1000px; height: 1200px; position: absolute; top: -385px; left: 50%; margin-left: -500px; border: none;"
            scrolling="no"></iframe>
    </div>
    """
    components.html(html_apeseg, height=480)

    st.markdown("---")

    # --- BLOQUE 2: PACÍFICO (Descarga de PDF) ---
    st.markdown("#### 📄 2. Descarga de Certificado (Pacífico)")
    st.caption("Si el vehículo es de Pacífico, usa este cuadro para bajar el PDF.")
    
    # Para evitar que Pacífico bloquee la conexión, usamos un puente (CORS Proxy)
    # Nota: He ajustado el 'top' para encuadrar el buscador de Pacífico
    html_pacifico = """
    <div style="width: 100%; height: 460px; overflow: hidden; border: 2px solid #0096d2; border-radius: 12px; position: relative; background: white;">
        <iframe src="https://www.pacifico.com.pe/consulta-soat" 
            style="width: 1000px; height: 1500px; position: absolute; top: -300px; left: 50%; margin-left: -500px; border: none;"
            scrolling="no"></iframe>
    </div>
    """
    components.html(html_pacifico, height=480)

    st.info("💡 Consejo: Una vez que consultes en el primer cuadro, desplázate hacia abajo para usar el segundo.")

if __name__ == "__main__":
    run()
