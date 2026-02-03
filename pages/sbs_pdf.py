import streamlit as st
import requests
import base64
from PIL import Image
import io

def run():
    st.markdown("<h1 style='text-align: center;'>🏦 Reporte de Deudas SBS</h1>", unsafe_allow_html=True)

    TOKEN = "sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"
    dni_input = st.text_input("Ingrese DNI para consulta SBS", max_chars=8, placeholder="45106211")

    if st.button("📊 GENERAR REPORTE SBS", use_container_width=True):
        if not dni_input:
            st.warning("Ingrese un DNI.")
            return

        url = "https://seeker-v6.com/personas/sbs_pdf_api"
        headers = {"Authorization": f"Bearer {TOKEN}"}
        payload = {"dni": dni_input}

        with st.spinner("Procesando formato oficial SBS..."):
            try:
                # Timeout largo porque este reporte consume 5 créditos y es pesado
                res = requests.post(url, headers=headers, json=payload, timeout=60)
                
                # Si el servidor responde con HTML de Login, es un error de sesión de la API
                if "text/html" in res.headers.get("Content-Type", ""):
                    st.error("❌ Error de Sesión: La API redirigió al Login. Intenta de nuevo en unos momentos.")
                    return

                data = res.json()

                if data.get("status") == "success":
                    st.success("✅ Datos recuperados")
                    
                    # Intentamos extraer el contenido independientemente del nombre de la llave
                    # Seeker a veces usa 'pdf' y otras veces 'base64' dentro de 'data'
                    contenido_raw = data.get("pdf") or data.get("data", {}).get("pdf") or data.get("data", {}).get("base64")

                    if contenido_raw:
                        # Convertimos a bytes para determinar si es imagen o PDF
                        file_bytes = base64.b64decode(contenido_raw)
                        
                        # --- VISUALIZADOR MULTI-FORMATO ---
                        if file_bytes.startswith(b'%PDF'):
                            # Si es PDF, usamos el conversor que ya tienes
                            from pdf2image import convert_from_bytes
                            images = convert_from_bytes(file_bytes, dpi=150)
                            for i, img in enumerate(images):
                                st.image(img, caption=f"Página {i+1}", use_container_width=True)
                        else:
                            # Si es imagen directa (JPG/PNG), la mostramos de una
                            st.image(file_bytes, caption="Reporte SBS Oficial", use_container_width=True)

                        # Botón de descarga universal
                        st.download_button(
                            label="📥 DESCARGAR REPORTE",
                            data=file_bytes,
                            file_name=f"SBS_{dni_input}.pdf", # Lo guardamos como PDF por estándar
                            mime="application/pdf"
                        )
                    else:
                        st.warning("La respuesta fue exitosa pero no contiene un archivo visualizable.")
                        st.json(data)
                else:
                    st.error(f"API Error: {data.get('message', 'DNI no encontrado')}")

            except Exception as e:
                st.error(f"Error en el formato: {str(e)}")

if __name__ == "__main__":
    run()
