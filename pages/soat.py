import streamlit as st
import time

def obtener_datos_soat_reales(placa):
    # Aquí es donde el script iría a APESEG, resolvería el captcha 
    # y traería el JSON con la info. Por ahora simulamos la data exitosa:
    # (Para esto necesitas una API Key de un 'Captcha Solver')
    time.sleep(2) # Simulando tiempo de proceso
    return {
        "compania": "INTERSEGURO",
        "estado": "VIGENTE",
        "inicio": "03/06/2025",
        "fin": "03/06/2026",
        "certificado": "594222744",
        "uso": "TAXI",
        "clase": "AUTOMOVIL"
    }

def run():
    st.markdown("<h2 style='text-align: center;'>📋 Generador de Reporte SOAT</h2>", unsafe_allow_html=True)
    
    placa = st.text_input("Ingrese la Placa", max_chars=6, placeholder="M3Z244").upper()

    if st.button("🚀 GENERAR FICHA OFICIAL", use_container_width=True):
        if placa:
            with st.spinner("Extrayendo datos de la base de datos nacional..."):
                datos = obtener_datos_soat_reales(placa)
                
                # --- TU PLANTILLA PERSONALIZADA ---
                st.markdown("---")
                st.success("✅ Conexión exitosa con la base de datos de seguros.")
                
                # Contenedor con diseño similar al que enviaste en tus fotos
                with st.container(border=True):
                    st.markdown(f"### 🚗 Información Vehicular: {placa}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f"**Compañía:** {datos['compania']}")
                        st.markdown(f"**Estado:** :green[{datos['estado']}]")
                        st.markdown(f"**Tipo de Uso:** {datos['uso']}")
                    
                    with col2:
                        st.markdown(f"**Fecha Inicio:** {datos['inicio']}")
                        st.markdown(f"**Fecha Fin:** {datos['fin']}")
                        st.markdown(f"**Certificado:** `{datos['certificado']}`")
                
                # Historial de certificados (como en tu imagen de Telegram)
                with st.expander("Ver Historial de Certificados SOAT"):
                    st.table([
                        {"Certificado": datos['certificado'], "Compañía": datos['compania'], "Estado": "ACTIVO"},
                        {"Certificado": "700341168", "Compañía": "Protecta", "Estado": "VENCIDO"}
                    ])
        else:
            st.warning("Por favor, digite una placa válida.")

if __name__ == "__main__":
    run()
