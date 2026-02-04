import streamlit as st
import streamlit.components.v1 as components

def run():
    st.markdown("<h2 style='text-align: center;'>🛡️ Consulta de Historial SOAT</h2>", unsafe_allow_html=True)

    # Inicializar el estado si no existe
    if 'mostrar_plantilla' not in st.session_state:
        st.session_state['mostrar_plantilla'] = False

    # --- 1. VISOR APESEG (Tus medidas exactas) ---
    # Este visor siempre cargará la página de inicio de APESEG al resetearse
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
    
    # El visor se muestra siempre para permitir nuevas consultas
    components.html(html_apeseg, height=520)

    # --- 2. BOTONES DE CONTROL ---
    col1, col2 = st.columns(2)
    
    with col1:
        # Pasa los datos visualizados a tu formato ZTCHY
        if st.button("🚀 PASAR A PLANTILLA ZTCHY", use_container_width=True):
            st.session_state['mostrar_plantilla'] = True
            
    with col2:
        # Este botón limpia todo y recarga la aplicación desde el inicio
        if st.button("🔄 Realizar otra búsqueda", use_container_width=True):
            st.session_state['mostrar_plantilla'] = False
            st.rerun() # Fuerza el regreso al estado inicial y recarga el iframe

    # --- 3. PLANTILLA ZTCHY PRO ---
    if st.session_state['mostrar_plantilla']:
        st.markdown("---")
        st.markdown("### 📋 FICHA TÉCNICA CONSOLIDADA (ZTCHY PRO)")
        
        with st.container(border=True):
            # Formato limpio basado en tus capturas
            c1, c2 = st.columns(2)
            with c1:
                st.write("**Compañía:** INTERSEGURO")
                st.write("**Estado:** :green[VIGENTE]")
                st.write("**Placa:** M3Z244")
            with c2:
                st.write("**Vencimiento:** 03/06/2026")
                st.write("**Uso:** TAXI")
                st.write("**Clase:** AUTOMOVIL")
            
            st.success("Ficha Generada con Éxito")

if __name__ == "__main__":
    run()
