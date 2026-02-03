import streamlit as st
import requests
from bs4 import BeautifulSoup

def run():
    st.markdown("<h1 style='text-align: center;'>📋 Reporte Vehicular Consolidado</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>Consulta Gratuita Independiente</p>", unsafe_allow_html=True)

    placa = st.text_input("Ingrese Placa (ej: ABC123)", max_chars=6).upper()

    if st.button("📊 GENERAR REPORTE DETALLADO", use_container_width=True):
        if not placa:
            st.error("Por favor, ingrese una placa.")
            return

        with st.spinner("Consultando múltiples fuentes oficiales..."):
            # Simulamos el puente a SUNARP y APESEG
            # En una fase avanzada, aquí usaríamos 'requests' para scrapear cada sitio
            
            # --- DISEÑO DE INFORMACIÓN DETALLADA ---
            tab1, tab2, tab3 = st.tabs(["🚗 Datos del Vehículo", "🛡️ Estado del SOAT", "👤 Propietario"])

            with tab1:
                st.subheader("Ficha Técnica (Fuente: SUNARP)")
                col1, col2 = st.columns(2)
                with col1:
                    st.write("**Marca:** TOYOTA")
                    st.write("**Modelo:** COROLLA")
                    st.write("**Año Fab.:** 2022")
                    st.write("**Color:** GRIS METÁLICO")
                with col2:
                    st.write("**Nro. Motor:** 1ZR-XXXXXX")
                    st.write("**Nro. Chasis:** 9AM-XXXXXX")
                    st.write("**Combustible:** GNV/GLP")
                    st.write("**Asientos:** 5")

            with tab2:
                st.subheader("Certificado de Seguro (Fuente: APESEG)")
                with st.container(border=True):
                    st.write(f"**Compañía:** PACIFICO SEGUROS")
                    st.write(f"**Certificado:** 77889922")
                    st.write(f"**Vigencia:** 🟢 VIGENTE")
                    st.write(f"**Desde:** 01/01/2026  **Hasta:** 01/01/2027")

            with tab3:
                st.subheader("Información de Titularidad")
                st.info("Información protegida por Ley de Datos Personales")
                st.write("**Propietario Actual:** RUIZ ZATOCHY, JUAN CARLOS")
                st.write("**Sede de Registro:** LIMA")

            st.success("✅ Reporte generado exitosamente sin uso de créditos.")

if __name__ == "__main__":
    run()
