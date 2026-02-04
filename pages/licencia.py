import streamlit as st
import streamlit.components.v1 as components

def run():
    st.set_page_config(page_title="Consulta SOAT PRO", layout="wide")
    
    st.markdown("<h2 style='text-align: center;'>🛡️ Sistema de Consulta SOAT</h2>", unsafe_allow_html=True)
    st.info("ℹ️ Complete la placa y el captcha en el visor de abajo. Una vez que vea los resultados, use el botón para capturarlos.")

    # --- BLOQUE 1: VISOR OFICIAL (Con tus medidas de recorte) ---
    # Mantenemos el recorte exacto para que el usuario solo vea el formulario
    with st.container():
        html_apeseg = """
        <div style="
            width: 100%; 
            height: 500px; 
            overflow: hidden; 
            border: 2px solid #1E3A8A; 
            border-radius: 12px; 
            position: relative; 
            background: white;
            margin-bottom: 20px;">
            
            <iframe src="https://www.apeseg.org.pe/consultas-soat/" 
                style="
                    width: 1300px; 
                    height: 1500px; 
                    position: absolute; 
                    top: -560px; 
                    left: 50%; 
                    margin-left: -615px; 
                    border: none;"
                scrolling="no">
            </iframe>
        </div>
        """
        components.html(html_apeseg, height=520)

    # --- BLOQUE 2: PANEL DE RESULTADOS (Opcional tras validar) ---
    # Aquí es donde el usuario confirma que ya vio la info en el visor
    if st.button("📋 GENERAR FICHA TÉCNICA DESDE RESULTADOS", use_container_width=True):
        st.success("✅ Datos capturados correctamente (Simulación basada en visor)")
        
        with st.expander("🔍 Ver Detalle Consolidado", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Compañía:** INTERSEGURO")
                st.markdown("**Estado:** :green[VIGENTE]")
            with col2:
                st.markdown("**Vencimiento:** 03/06/2026")
                st.markdown("**Certificado:** Digital")

if __name__ == "__main__":
    run()
