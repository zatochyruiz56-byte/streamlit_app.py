import streamlit as st
import requests
import base64
from pdf2image import convert_from_bytes
import io

def run():
    st.markdown("<h1 style='text-align: center;'>🪪 Visor de Ficha Antidetección</h1>", unsafe_allow_html=True)

    TOKEN = "sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"
    dni_input = st.text_input("DNI para consulta", max_chars=8)

    if st.button("👁️ VER FICHA AHORA", use_container_width=True):
        if not dni_input:
            st.warning("Escribe un DNI.")
            return

        url = "https://seeker-v6.com/personas/api/ficha"
        headers = {"Authorization": f"Bearer {TOKEN}"}
        payload = {"dni": dni_input}

        with st.spinner("Transformando PDF a imagen para saltar bloqueos..."):
            try:
                res = requests.post(url, headers=headers, json=payload)
                data = res.json()

                if data.get("status") == "success":
                    pdf_b64 = data.get("pdf")
                    pdf_bytes = base64.b64decode(pdf_b64)

                    # --- EL TRUCO MAGICO: PDF A IMAGEN ---
                    # Convertimos la primera página del PDF en una imagen
                    images = convert_from_bytes(pdf_bytes)
                    
                    if images:
                        # Mostramos la imagen (Esto no lo bloquea Chrome)
                        st.success("✅ Documento renderizado con éxito")
                        
                        # Botón para descargar el PDF Original (el archivo real)
                        st.download_button(
                            label="📥 DESCARGAR PDF ORIGINAL",
                            data=pdf_bytes,
                            file_name=f"Ficha_{dni_input}.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )

                        # Mostrar la imagen del documento
                        for img in images:
                            st.image(img, use_container_width=True, caption="Vista previa oficial")
                    
                else:
                    st.error("No se pudo obtener el documento.")
            except Exception as e:
                st.error("Error: Asegúrate de tener 'pdf2image' instalado.")
                st.info("Nota: Este método requiere poppler instalado en el servidor.")

if __name__ == "__main__":
    run()
