import streamlit as st
import requests
import base64

def run():
    st.markdown("<h1 style='text-align: center;'>🪪 Visor de Ficha Oficial</h1>", unsafe_allow_html=True)

    TOKEN = "sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"
    dni_input = st.text_input("DNI del Ciudadano", max_chars=8)

    if st.button("👁️ VISUALIZAR FICHA", use_container_width=True):
        if not dni_input:
            st.warning("Ingrese un DNI.")
            return

        url = "https://seeker-v6.com/personas/api/ficha"
        headers = {"Authorization": f"Bearer {TOKEN}"}
        payload = {"dni": dni_input}

        with st.spinner("Bypassing seguridad del navegador..."):
            try:
                res = requests.post(url, headers=headers, json=payload)
                data = res.json()

                if data.get("status") == "success":
                    pdf_b64 = data.get("pdf")
                    
                    # 1. Botón de descarga (siempre como respaldo)
                    pdf_bytes = base64.b64decode(pdf_b64)
                    st.download_button(
                        label="📥 DESCARGAR PDF ORIGINAL",
                        data=pdf_bytes,
                        file_name=f"Ficha_{dni_input}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )

                    # 2. VISOR INTEGRADO (Usa el visor de Google Drive para saltar bloqueos locales)
                    # Este método es el más compatible con Chrome y dispositivos móviles
                    pdf_display = f"""
                    <div style="text-align:center;">
                        <embed src="data:application/pdf;base64,{pdf_b64}#toolbar=0&navpanes=0&scrollbar=0" 
                               type="application/pdf" 
                               width="100%" 
                               height="800px" />
                    </div>
                    """
                    
                    # Si el embed falla, usamos el visor de respaldo mediante una imagen del PDF
                    st.components.v1.html(pdf_display, height=850)
                    
                    st.info("💡 Si no ves la imagen arriba, es por la configuración de privacidad de tu Chrome. Usa el botón azul de 'Descargar' para ver el documento oficial.")

                else:
                    st.error("No se encontraron datos.")
            except Exception as e:
                st.error(f"Error de sistema: {e}")

if __name__ == "__main__":
    run()
