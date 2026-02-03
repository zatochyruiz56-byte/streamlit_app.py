import streamlit as st
import requests
import base64

def run():
    st.markdown("<h1 style='text-align: center;'>🪪 Ficha RENIEC Premium</h1>", unsafe_allow_html=True)

    TOKEN = "sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"
    dni_input = st.text_input("Ingrese DNI", max_chars=8)

    if st.button("📄 GENERAR VISTA PREVIA", use_container_width=True):
        if not dni_input:
            st.warning("Ingrese un DNI.")
            return

        url = "https://seeker-v6.com/personas/api/ficha"
        payload = {"dni": dni_input}
        headers = {"Authorization": f"Bearer {TOKEN}"}

        with st.spinner("Bypass de seguridad y cargando PDF..."):
            try:
                res = requests.post(url, headers=headers, json=payload)
                data = res.json()

                if data.get("status") == "success":
                    pdf_b64 = data.get("pdf")
                    pdf_bytes = base64.b64decode(pdf_b64)

                    # 1. Botón de Descarga Tradicional (Siempre funciona)
                    st.download_button(
                        label="📥 DESCARGAR PDF",
                        data=pdf_bytes,
                        file_name=f"Ficha_{dni_input}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )

                    # 2. TRUCO DE BYPASS: JavaScript Blob URL
                    # Esto engaña al navegador para que crea que el PDF es un archivo local
                    components_html = f"""
                    <div id="pdf-container" style="height: 800px; border: 1px solid #ccc;">
                        <p id="loading-text" style="text-align:center; padding-top:20px;">Cargando visor oficial...</p>
                    </div>

                    <script>
                        (function() {{
                            const base64Data = "{pdf_b64}";
                            const byteCharacters = atob(base64Data);
                            const byteNumbers = new Array(byteCharacters.length);
                            for (let i = 0; i < byteCharacters.length; i++) {{
                                byteNumbers[i] = byteCharacters.charCodeAt(i);
                            }}
                            const byteArray = new Uint8Array(byteNumbers);
                            const blob = new Blob([byteArray], {{type: 'application/pdf'}});
                            const blobUrl = URL.createObjectURL(blob);

                            const container = document.getElementById('pdf-container');
                            container.innerHTML = `<iframe src="${{blobUrl}}" width="100%" height="100%" style="border:none;"></iframe>`;
                        }})();
                    </script>
                    """
                    
                    st.components.v1.html(components_html, height=850)

                else:
                    st.error("DNI no encontrado.")
            except Exception as e:
                st.error(f"Error: {e}")

if __name__ == "__main__":
    run()
