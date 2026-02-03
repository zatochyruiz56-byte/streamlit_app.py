import streamlit as st
import pandas as pd

def mostrar_reporte_completo(placa, datos):
    # Título Estilizado
    st.markdown(f"<h2 style='text-align: center; color: #1E3A8A;'>🚗 Ficha Técnica Vehicular: {placa}</h2>", unsafe_allow_html=True)
    st.success("✅ Conexión exitosa con la base de datos nacional (APESEG/Interseguro).")

    # --- SECCIÓN 1: VIGENCIA Y ESTADO ACTUAL ---
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Estado del SOAT", value=datos['estado'])
    with col2:
        st.metric(label="Días Restantes", value=datos['días_restantes'])
    with col3:
        st.metric(label="Compañía Actual", value=datos['compania'])

    # --- SECCIÓN 2: DETALLES DE LA PÓLIZA (Cuadro Principal) ---
    with st.container(border=True):
        st.markdown("#### 📄 Información Detallada del Certificado")
        c1, c2 = st.columns(2)
        with c1:
            st.write(f"**N° de Póliza/Certificado:** `{datos['certificado']}`")
            st.write(f"**Fecha de Inicio:** {datos['inicio']}")
            st.write(f"**Fecha de Vencimiento:** {datos['fin']}")
            st.write(f"**Fecha de Creación:** {datos['fecha_creacion']}")
        with c2:
            st.write(f"**Uso del Vehículo:** {datos['uso']}")
            st.write(f"**Clase/Categoría:** {datos['clase']}")
            st.write(f"**Tipo de SOAT:** {datos['tipo']}")
            st.write(f"**Hora de Emisión:** {datos['hora_emision']}")

    # --- SECCIÓN 3: LÍNEA DE TIEMPO (Visualización de Vigencia) ---
    st.markdown("#### ⏳ Línea de Tiempo de Cobertura")
    # Simulación de la barra de progreso que viste en tu imagen de referencia
    progreso = 0.65 # Ejemplo: 65% del tiempo transcurrido
    st.progress(progreso)
    st.caption(f"Emisión: {datos['inicio']} ----------------------------------- Hoy ----------------------------------- Vence: {datos['fin']}")

    # --- SECCIÓN 4: HISTORIAL DE CERTIFICADOS (Tabla) ---
    st.markdown("#### 📜 Historial de Certificados SOAT")
    df_historial = pd.DataFrame(datos['historial'])
    st.table(df_historial) # Muestra el historial completo como en tu imagen

    # --- BOTONES DE ACCIÓN ---
    st.download_button(
        label="📥 Descargar Constancia PDF",
        data="Contenido_binario_del_PDF",
        file_name=f"CERTIFICADO_SOAT_{placa}.pdf",
        mime="application/pdf"
    )

# --- DATOS DE EJEMPLO (Lo que tu scraper debe extraer) ---
datos_vivos = {
    "placa": "M3Z244",
    "estado": "VIGENTE",
    "días_restantes": "119 Días",
    "compania": "INTERSEGURO",
    "certificado": "0000000000000594222744",
    "inicio": "03/06/2025",
    "fin": "03/06/2026",
    "fecha_creacion": "03/06/2025 08:08",
    "hora_emision": "17:35",
    "uso": "TAXI",
    "clase": "AUTOMOVIL",
    "tipo": "DIGITAL",
    "historial": [
        {"Certificado": "594222744", "Compañía": "INTERSEGURO", "Estado": "ACTIVO", "Vence": "03/06/2026"},
        {"Certificado": "00593549960", "Compañía": "INTERSEGURO", "Estado": "VENCIDO", "Vence": "03/06/2025"},
        {"Certificado": "700341168", "Compañía": "PROTECTA", "Estado": "VENCIDO", "Vence": "03/06/2024"}
    ]
}

# Ejecución
if st.button("OBTENER INFORMACIÓN COMPLETA"):
    mostrar_reporte_completo("M3Z244", datos_vivos)
