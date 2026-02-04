import streamlit as st
import streamlit.components.v1 as components

def run():
    st.markdown("<h2 style='text-align: center;'>🛡️ Sistema de Validación ZTCHY</h2>", unsafe_allow_html=True)

    # --- PASO 1: CONSULTA ORIGINAL (Tus medidas) ---
    st.markdown("### 🔍 1. Validación en Fuente Oficial")
    
    # Creamos dos columnas: una para el visor y otra para tu nueva plantilla
    col_visor, col_plantilla = st.columns([1.2, 1])

    with col_visor:
        # Tus medidas exactas: top: -560px, left: 60%
        html_apeseg = """
        <div style="width: 100%; height: 480px; overflow: hidden; border: 2px solid #ddd; border-radius: 8px; position: relative;">
            <iframe src="https://www.apeseg.org.pe/consultas-soat/" 
                style="width: 1000px; height: 1500px; position: absolute; top: -560px; left: 60%; margin-left: -400px; border: none;"
                scrolling="no"></iframe>
        </div>
        """
        components.html(html_apeseg, height=500)
        
        if st.button("🔄 Nueva Búsqueda", use_container_width=True):
            st.rerun()

    with col_plantilla:
        st.markdown("### 📝 2. Generar Ficha ZTCHY")
        st.write("Una vez veas los resultados a la izquierda, confírmalos aquí:")
        
        # Formulario rápido para "atrapar" los datos en tu plantilla
        with st.form("ficha_pro"):
            compania = st.selectbox("Compañía Detectada", ["Interseguro", "Pacífico", "Rimac", "La Positiva"])
            estado = st.radio("Estado del SOAT", ["VIGENTE 🟢", "VENCIDO 🔴"], horizontal=True)
            vence = st.date_input("Fecha de Vencimiento")
            
            if st.form_submit_button("🚀 GENERAR REPORTE LIMPIO"):
                # Aquí es donde el sistema "detecta" y te da tu propia plantilla
                st.success("Ficha Generada con Éxito")
                st.markdown(f"""
                <div style="padding: 20px; border: 2px solid #1E3A8A; border-radius: 10px; background: #f0f2f6;">
                    <h4 style="margin:0;">CERTIFICADO DE VALIDACIÓN</h4>
                    <hr>
                    <p><b>Aseguradora:</b> {compania}</p>
                    <p><b>Estado:</b> {estado}</p>
                    <p><b>Vencimiento:</b> {vence}</p>
                    <p style="font-size: 10px; color: gray;">Validado por ZTCHY PRO - {st.session_state.get('placa', 'M3Z244')}</p>
                </div>
                """, unsafe_allow_html=True)

if __name__ == "__main__":
    run()
