import streamlit as st
import streamlit.components.v1 as components

def run():
    st.markdown("<h2 style='text-align: center; color: #1E3A8A;'>🛡️ Central de Consultas SOAT</h2>", unsafe_allow_html=True)

    # --- BLOQUE 1: APESEG (Tus medidas personalizadas) ---
    st.markdown("### 📊 1. Historial y Vigencia")
    # Aplicamos tus coordenadas exactas: top: -560px, left: 60%, margin-left: -400px
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

    # --- BLOQUE 2: ZONA DE DESCARGA (Instrucciones de obtención) ---
    st.markdown("### 📄 2. Obtención de Certificado Digital")
    
    with st.expander("📝 Pasos para descargar el PDF sin salir de la app", expanded=True):
        st.write("Debido a las restricciones de seguridad de las aseguradoras, sigue estos pasos:")
        st.markdown("""
        1. Consulta la placa en el recuadro de arriba (**APESEG**).
        2. Identifica la **Compañía** (Ej: Interseguro, Pacífico).
        3. Si necesitas el PDF, usa el visor oficial seguro aquí debajo:
        """)
        
        # Este enlace abre la zona de descarga en un marco más grande para intentar forzar la carga
        st.link_button("🚀 Abrir Visor de Descarga Oficial", "https://www.interseguro.pe/soat/consulta-soat", use_container_width=True)

    st.caption("⚠️ Las protecciones de dominio impiden el espejo directo en la zona de certificados.")

if __name__ == "__main__":
    run()
