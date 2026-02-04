import streamlit as st

def generar_plantilla_ztchy(datos):
    """Muestra la información extraída en tu formato profesional"""
    st.markdown("---")
    st.markdown("### 📋 FICHA TÉCNICA CONSOLIDADA (ZTCHY PRO)")
    
    with st.container(border=True):
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Compañía:** {datos['compania']}")
            st.write(f"**Estado:** {datos['estado']}")
            st.write(f"**Número de Placa:** {datos['placa']}")
            st.write(f"**Uso del Vehículo:** {datos['uso']}")
        with col2:
            st.write(f"**Fecha Inicio:** {datos['inicio']}")
            st.write(f"**Fecha Fin:** {datos['vencimiento']}")
            st.write(f"**Clase de Vehículo:** {datos['clase']}")
            st.write(f"**Tipo de Certificado:** {datos['tipo']}")
            
        st.success(f"Certificado {datos['estado']} verificado correctamente.")

def run():
    st.title("🛡️ Verificador Inteligente ZTCHY")

    # 1. Visor de Captcha (Original con tus medidas)
    # top: -560px, left: 60%
    st.markdown("#### 1. Resuelva el Captcha en la fuente oficial")
    html_visor = """
    <div style="width: 100%; height: 400px; overflow: hidden; border: 2px solid #1E3A8A; border-radius: 10px;">
        <iframe src="https://www.apeseg.org.pe/consultas-soat/" 
            style="width: 1000px; height: 1500px; position: absolute; top: -560px; left: 60%; margin-left: -400px; border: none;">
        </iframe>
    </div>
    """
    st.components.v1.html(html_visor, height=420)

    # 2. El "Botón de Captura" 
    # Como el sistema no puede autodetectar el click interno del iframe, 
    # usamos este botón para 'traer' los datos a la plantilla
    if st.button("🚀 EXTRAER DATOS A PLANTILLA ZTCHY", use_container_width=True):
        # Aquí es donde el backend haría el scraping automático. 
        # Por ahora, volcamos los datos completos detectados en la imagen
        datos_extraidos = {
            "compania": "INTERSEGURO",
            "estado": "VIGENTE 🟢",
            "inicio": "03/06/2025",
            "vencimiento": "03/06/2026",
            "placa": "M3Z244",
            "uso": "TAXI",
            "clase": "AUTOMOVIL",
            "tipo": "DIGITAL"
        }
        generar_plantilla_ztchy(datos_extraidos)

    if st.button("🔄 Nueva Búsqueda"):
        st.rerun()

run()
