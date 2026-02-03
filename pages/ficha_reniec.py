import streamlit as st
import requests

def run():
    st.markdown("<h1 style='text-align: center;'>🪪 Consulta de Ficha RENIEC</h1>", unsafe_allow_html=True)

    TOKEN = "sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"
    dni_input = st.text_input("Ingrese DNI para generar ficha", max_chars=8, placeholder="Ejm: 45106211")

    if st.button("📄 GENERAR FICHA OFICIAL", use_container_width=True):
        if not dni_input:
            st.warning("Por favor, ingrese un DNI válido.")
            return

        url = "https://seeker-v6.com/personas/api/ficha"
        headers = {"Authorization": f"Bearer {TOKEN}"}
        # Según la documentación, este servicio usa POST con un JSON
        payload = {"dni": dni_input}

        with st.spinner("Accediendo a la base de datos de identidad..."):
            try:
                res = requests.post(url, headers=headers, json=payload)
                
                if res.status_code == 200:
                    data = res.json()
                    if data.get("status") == "success":
                        info = data.get("data", {})
                        
                        st.success("✅ Datos recuperados correctamente")

                        # --- DISEÑO DE LA FICHA (Sin marcas de agua) ---
                        ficha_html = f"""
                        <!DOCTYPE html>
                        <html>
                        <head>
                            <style>
                                .ficha-container {{
                                    font-family: Arial, sans-serif;
                                    border: 2px solid #1e293b;
                                    padding: 30px;
                                    max-width: 800px;
                                    margin: auto;
                                    background: white;
                                    color: #1e293b;
                                }}
                                .header {{
                                    text-align: center;
                                    border-bottom: 2px solid #1e293b;
                                    margin-bottom: 20px;
                                    padding-bottom: 10px;
                                }}
                                .data-row {{
                                    display: flex;
                                    justify-content: space-between;
                                    margin-bottom: 12px;
                                    border-bottom: 1px solid #e2e8f0;
                                    padding-bottom: 5px;
                                }}
                                .label {{ font-weight: bold; color: #64748b; text-transform: uppercase; font-size: 0.8em; }}
                                .value {{ font-weight: bold; font-size: 1.1em; }}
                                @media print {{ .no-print {{ display: none; }} }}
                            </style>
                        </head>
                        <body>
                            <div class="ficha-container">
                                <div class="header">
                                    <h2 style="margin:0;">FICHA DE INSCRIPCIÓN DE IDENTIDAD</h2>
                                    <p style="margin:5px; color: #64748b;">DOCUMENTO PRIVADO - CONSULTA DNI {dni_input}</p>
                                </div>
                                
                                <div class="data-row"><span class="label">Nombres</span><span class="value">{info.get('nombres', '---')}</span></div>
                                <div class="data-row"><span class="label">Primer Apellido</span><span class="value">{info.get('apellido_paterno', '---')}</span></div>
                                <div class="data-row"><span class="label">Segundo Apellido</span><span class="value">{info.get('apellido_materno', '---')}</span></div>
                                <div class="data-row"><span class="label">Fecha de Nacimiento</span><span class="value">{info.get('fecha_nacimiento', '---')}</span></div>
                                <div class="data-row"><span class="label">Sexo</span><span class="value">{info.get('sexo', '---')}</span></div>
                                <div class="data-row"><span class="label">Estado Civil</span><span class="value">{info.get('estado_civil', '---')}</span></div>
                                <div class="data-row"><span class="label">Ubicación</span><span class="value">{info.get('ubigeo_completo', '---')}</span></div>
                                <div class="data-row"><span class="label">Dirección Actual</span><span class="value">{info.get('direccion', '---')}</span></div>
                                <div class="data-row"><span class="label">Grado de Instrucción</span><span class="value">{info.get('grado_instruccion', '---')}</span></div>
                                
                                <script>window.onload = function() {{ if(window.location.search.includes('print')) window.print(); }}</script>
                            </div>
                        </body>
                        </html>
                        """

                        # Botón para descargar/imprimir PDF
                        st.download_button(
                            label="📥 DESCARGAR FICHA PDF",
                            data=pdf_html_trigger(ficha_html),
                            file_name=f"Ficha_RENIEC_{dni_input}.html",
                            mime="text/html"
                        )

                        # Vista previa
                        st.components.v1.html(ficha_html, height=600)
                    else:
                        st.error(f"Error: {data.get('message', 'DNI no encontrado')}")
                else:
                    st.error("Error de comunicación con el servidor.")
            except Exception as e:
                st.error(f"Error técnico: {e}")

def pdf_html_trigger(content):
    # Añade el script de impresión automática para que el navegador genere el PDF
    return content.replace("</body>", "<script>window.print();</script></body>")

if __name__ == "__main__":
    run()
