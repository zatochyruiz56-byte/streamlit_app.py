import streamlit as st
import requests
import re

def run():
    st.markdown("<h1 style='text-align: center;'>🌳 Generador de Reportes Genealógicos</h1>", unsafe_allow_html=True)

    TOKEN = "sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"
    dni_input = st.text_input("DNI del Titular", max_chars=8)

    if st.button("🔍 GENERAR Y LIMPIAR ÁRBOL", use_container_width=True):
        if not dni_input:
            st.warning("Ingrese un DNI.")
            return

        url = "https://seeker-v6.com/personas/arbol-visualApi"
        headers = {"Authorization": f"Bearer {TOKEN}"}
        params = {"dni": dni_input}

        with st.spinner("Procesando árbol y eliminando marcas de agua..."):
            try:
                res = requests.get(url, headers=headers, params=params)
                if res.status_code == 200:
                    data = res.json()
                    if data.get("status") == "success":
                        svg_raw = data.get("svg")

                        # --- 🛡️ MÓDULO DE LIMPIEZA (Anti-Marca de Agua) ---
                        # Eliminamos textos que contengan "Seeker", "Telegram" o nombres de la API
                        # Usamos expresiones regulares para borrar esas etiquetas del SVG
                        svg_clean = re.sub(r'<text[^>]*>.*?Seeker.*?</text>', '', svg_raw, flags=re.IGNORECASE)
                        svg_clean = re.sub(r'<text[^>]*>.*?Telegram.*?</text>', '', svg_clean, flags=re.IGNORECASE)
                        svg_clean = re.sub(r'<image[^>]*seeker[^>]*/>', '', svg_clean, flags=re.IGNORECASE)
                        
                        st.success("✅ Árbol generado sin marcas de agua.")

                        # --- 📄 OPCIÓN DE DESCARGA PDF ---
                        # Creamos un contenedor HTML para el PDF
                        html_report = f"""
                        <div id="printarea" style="background:white; padding:20px;">
                            <h2 style="text-align:center; font-family:Arial;">REPORTE GENEALÓGICO OFICIAL</h2>
                            <hr>
                            {svg_clean}
                        </div>
                        """
                        
                        # Botón para descargar/imprimir
                        st.download_button(
                            label="📥 DESCARGAR REPORTE PDF",
                            data=html_report,
                            file_name=f"Reporte_{dni_input}.html",
                            mime="text/html",
                            help="Se descargará un archivo que puedes guardar como PDF desde tu navegador (Ctrl+P)"
                        )

                        # Visualización en la App
                        st.components.v1.html(html_report, height=1000, scrolling=True)

                    else:
                        st.error("No se pudo obtener el gráfico.")
                else:
                    st.error("Error en el servidor.")
            except Exception as e:
                st.error(f"Error técnico: {e}")

if __name__ == "__main__":
    run()
