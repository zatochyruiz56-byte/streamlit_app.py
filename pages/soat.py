import streamlit as st
import time

# --- FUNCIÓN DE EXTRACCIÓN (Backend Invisible) ---
def extraer_data_oficial(placa):
    # Aquí es donde el código iría a la web oficial con un Captcha Solver
    # Por ahora, simulamos la respuesta detallada que obtendrías
    time.sleep(1.5) # Simula el tiempo de la "llave" del captcha
    return {
        "estado": "VIGENTE",
        "compania": "INTERSEGURO",
        "inicio": "03/06/2025",
        "fin": "03/06/2026",
        "certificado": "594222744",
        "uso": "TAXI",
        "clase": "AUTOMOVIL",
        "historial": [
            {"Certificado": "594222744", "Cía": "INTERSEGURO", "Vence": "03/06/2026", "Estado": "ACTIVO"},
            {"Certificado": "00593549960", "Cía": "INTERSEGURO", "Vence": "03/06/2025", "Estado": "VENCIDO"},
            {"Certificado": "700341168", "Cía": "PROTECTA", "Vence": "03/06/2024", "Estado": "VENCIDO"}
        ]
    }

# --- DISEÑO DE TU PÁGINA ---
st.markdown("<h2 style='text-align: center; color: #1E3A8A;'>🛡️ Sistema de Consulta SOAT</h2>", unsafe_allow_html=True)

# Cuadro de búsqueda propio
with st.container(border=True):
    placa_input = st.text_input("Ingrese Placa del Vehículo", placeholder="M3Z244", max_chars=6).upper()
    boton_consultar = st.button("🔍 GENERAR REPORTE COMPLETO", use_container_width=True)

if boton_consultar:
    if not placa_input:
        st.error("❌ Por favor, ingrese una placa.")
    else:
        with st.spinner("Conectando con la base de datos nacional..."):
            # 1. El código va por detrás, resuelve el captcha y trae la info
            data = extraer_data_oficial(placa_input)
            
            # 2. Mostramos el resultado en TU PLANTILLA
            st.markdown("---")
            st.balloons()
            
            # Encabezado de resultado
            st.markdown(f"### 📋 Reporte Detallado: {placa_input}")
            
            # Ficha Técnica
            with st.container(border=True):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Estado:** :green[{data['estado']}]")
                    st.write(f"**Aseguradora:** {data['compania']}")
                    st.write(f"**Uso:** {data['uso']}")
                with col2:
                    st.write(f"**Inicio:** {data['inicio']}")
                    st.write(f"**Vencimiento:** {data['fin']}")
                    st.write(f"**N° Certificado:** `{data['certificado']}`")

            # Tabla de Historial (Como la que querías)
            st.markdown("#### 📜 Historial de Certificados")
            st.table(data['historial'])

            # Botón de descarga simulado
            st.download_button("📥 Descargar Certificado PDF", data="pdf_data", file_name=f"SOAT_{placa_input}.pdf")
