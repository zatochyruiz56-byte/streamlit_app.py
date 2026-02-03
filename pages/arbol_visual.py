import streamlit as st
import requests
import re

def run():
    st.markdown("<h1 style='text-align: center;'>🌳 Generador de Reportes Genealógicos</h1>", unsafe_allow_html=True)

    TOKEN = "sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"
    dni_input = st.text_input("DNI del Titular", max_chars=8)

    if st.button("🔍 GENERAR REPORTE LIMPIO", use_container_width=True):
        if not dni_input:
            st.warning("Ingrese un DNI.")
            return

        url = "https://seeker-v6.com/personas/arbol-visualApi"
        headers = {"Authorization": f"Bearer {TOKEN}"}
        params = {"dni": dni_input}

        with st.spinner("Limpiando marcas de agua y preparando PDF..."):
            try:
                res = requests.get(url, headers=headers, params=params)
                if res.status_code == 200:
                    data = res.json()
                    svg_raw = data.get("svg", "")

                    # --- 🛡️ ELIMINACIÓN DE MARCA DE AGUA (Robot y Textos) ---
                    # 1. Borramos el logo del robot (etiqueta <use> o <image> con ID del logo)
                    svg_clean = re.sub(r'<g id="seeker-logo">.*?</g>', '', svg_raw, flags=re.IGNORECASE | re.DOTALL)
                    # 2. Borramos cualquier texto que mencione a Seeker o Telegram
                    svg_clean = re.sub(r'<text[^>]*>.*?Seeker.*?</text>', '', svg_clean, flags=re.IGNORECASE)
                    svg_clean = re.sub(r'<text[^>]*>.*?Telegram.*?</text>', '', svg_clean, flags=re.IGNORECASE)
                    # 3. Borramos el ID del símbolo del logo si existe
                    svg_clean = re.sub(r'<symbol id="robot-logo">.*?</symbol>', '', svg_clean, flags=re.IGNORECASE | re.DOTALL)

                    # --- 📄 PREPARACIÓN DEL DOCUMENTO PDF ---
                    # Este HTML tiene un script que activa la impresora al abrirse
                    pdf_html = f"""
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <title>Reporte_{dni_input}</title>
                        <style>
                            body {{ font-family: sans-serif; text-align: center; }}
                            .header {{ margin-bottom: 20px; border-bottom: 2px solid #333; padding: 10px; }}
                            @media print {{
                                .no-print {{ display: none; }}
                            }}
                        </style>
                    </head>
                    <body>
                        <div class="header">
                            <h1>INFORME GENEALÓGICO PRIVADO</h1>
                            <p>DNI CONSULTADO: {dni_input}</p>
                        </div>
                        {svg_clean}
                        <script>
                            // Este comando abre el cuadro de "Guardar como PDF" automáticamente
                            window.onload = function() {{ window.print(); }}
                        </script>
                    </body>
                    </html>
                    """
                    
                    st.success("✅ Árbol generado y marcas de agua eliminadas.")

                    # Botón de Descarga
                    st.download_button(
                        label="📥 DESCARGAR REPORTE PARA PDF",
                        data=pdf_html,
                        file_name=f"Reporte_{dni_input}.html",
                        mime="text/html",
                        help="Al abrir este archivo, se abrirá automáticamente la opción para Guardar como PDF."
                    )

                    # Vista previa en la web
                    st.components.v1.html(f"<div style='background:white; padding:10px;'>{svg_clean}</div>", height=1000, scrolling=True)

                else:
                    st.error("Error al conectar con la API.")
            except Exception as e:
                st.error(f"Ocurrió un error: {e}")

if __name__ == "__main__":
    run()
