import streamlit as st
import streamlit.components.v1 as components

def run():
    st.markdown("<h2 style='text-align: center;'>🛡️ Consulta de Historial SOAT</h2>", unsafe_allow_html=True)

    # 1. Lógica de Control de Estado
    if 'mostrar_plantilla' not in st.session_state:
        st.session_state['mostrar_plantilla'] = False

    # --- 2. EL VISOR (Tus medidas exactas) ---
    # Al recargar, el iframe vuelve siempre a la URL base de APESEG
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

    # --- 3. BOTONES CON REACCIÓN INSTANTÁNEA ---
    col1, col2 = st.columns(2)
    
    with col1:
        # Activa la visualización de tu plantilla
        if st.button("🚀 PASAR A PLANTILLA ZTCHY", use_container_width=True):
            st.session_state['mostrar_plantilla'] = True
            st.rerun() # Forzamos refresco para mostrar el cambio abajo
            
    with col2:
        # LIMPIEZA TOTAL: Borra la plantilla y reinicia el iframe
        if st.button("🔄 Realizar otra búsqueda", use_container_width=True):
            st.session_state['mostrar_plantilla'] = False
            # Borramos cualquier rastro de datos en la sesión para que la plantilla desaparezca
            for key in st.session_state.keys():
                st.session_state[key] = False
            st.rerun() 

    # --- 4. PLANTILLA ZTCHY (Solo aparece si se solicita) ---
    if st.session_state.get('mostrar_plantilla'):
        st.markdown("---")
        st.markdown("### 📋 FICHA TÉCNICA CONSOLIDADA (ZTCHY PRO)")
        
        # Esta sección desaparece por completo al dar clic en 'Realizar otra búsqueda'
        with st.container(border=True):
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
