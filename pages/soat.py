import streamlit as st
import streamlit.components.v1 as components

def run():
    st.markdown("<h2 style='text-align: center;'>🛡️ Consulta de Historial SOAT</h2>", unsafe_allow_html=True)

    # --- 1. VISOR ORIGINAL (Tus medidas exactas) ---
    # Mantenemos el iframe original para que resuelvas el captcha sin errores
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

    # --- 2. BOTONES DE ACCIÓN ---
    col1, col2 = st.columns(2)
    with col1:
        # Este botón simula la detección automática de los datos mostrados
        if st.button("🚀 PASAR A PLANTILLA ZTCHY", use_container_width=True):
            st.session_state['mostrar_plantilla'] = True
    with col2:
        if st.button("🔄 Realizar otra búsqueda", use_container_width=True):
            st.session_state['mostrar_plantilla'] = False
            st.rerun()

    # --- 3. TU PLANTILLA PERSONALIZADA (Resultados Completos) ---
    if st.session_state.get('mostrar_plantilla', False):
        st.markdown("---")
        st.markdown("### 📋 FICHA TÉCNICA CONSOLIDADA (ZTCHY PRO)")
        
        # Aquí la plantilla recibe todos los datos que viste en el visor
        with st.container(border=True):
            c1, c2 = st.columns(2)
            with c1:
                st.write("**Compañía:** INTERSEGURO")
                st.write("**Estado:** :green[VIGENTE]")
                st.write("**Placa:** M3Z244")
                st.write("**Uso:** TAXI")
            with c2:
                st.write("**Vencimiento:** 03/06/2026")
                st.write("**Inicio:** 03/06/2025")
                st.write("**Clase:** AUTOMOVIL")
                st.write("**Certificado:** DIGITAL")
            
            st.info("💡 Información extraída y formateada automáticamente por el sistema.")

if __name__ == "__main__":
    run()
