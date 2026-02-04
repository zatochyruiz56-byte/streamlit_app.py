import streamlit as st
import streamlit.components.v1 as components

def run():
    st.markdown("<h2 style='text-align: center; color: #1E3A8A;'>🛡️ Consulta SOAT Instantánea</h2>", unsafe_allow_html=True)

    # --- BLOQUE 1: APESEG (Restaurado con tus medidas exactas) ---
    st.markdown("### 📊 1. Buscador de Vigencia e Historial")
    # Aplicamos tus medidas: top: -560px, left: 60%, margin-left: -400px
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

    st.markdown("---")

    # --- BLOQUE 2: ACCESO A DESCARGA DE PDF ---
    st.markdown("### 📄 2. Obtener Certificado Electrónico (PDF)")
    st.info("Para evitar bloqueos de seguridad, utiliza estos enlaces directos que abren en una pestaña nueva.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.link_button("📥 Descargar de Interseguro", "https://www.interseguro.pe/soat/consulta-soat", use_container_width=True)
    with col2:
        st.link_button("📥 Descargar de Pacífico", "https://www.pacifico.com.pe/consulta-soat", use_container_width=True)

    st.caption("⚠️ Nota: Las aseguradoras no permiten mostrar su zona de descarga dentro de otras apps por seguridad.")

if __name__ == "__main__":
    run()
