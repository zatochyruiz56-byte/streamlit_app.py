import streamlit as st
import requests
import base64
from pdf2image import convert_from_bytes

def run():
    st.markdown("<h1 style='text-align: center;'>🏦 Reporte de Deudas SBS</h1>", unsafe_allow_html=True)

    TOKEN = "sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"
    dni_input = st.text_input("Ingrese DNI para consulta SBS", max_chars=8, placeholder="45106211")

    if st.button("📊 GENERAR REPORTE SBS", use_container_width=True):
        if not dni_input:
            st.warning("Por favor, ingrese un DNI.")
            return

        # Endpoint según tu documentación
        url = "https://seeker-v6.com/personas/sbs_pdf_api"
        headers = {"Authorization": f"Bearer {TOKEN}"}
        payload = {"dni": dni_input}

        with st.spinner("Consultando base de datos financiera..."):
            try:
                res = requests.post(url, headers=headers, json=payload)
                data = res.json()

                if data.get("status") == "success":
                    # Extraemos el PDF (usualmente viene dentro de data['pdf'] o data['data']['pdf'])
                    # Ajustamos según el estándar de Seeker
                    pdf_b64 = data.get("pdf") or data.get("data", {}).get("pdf")
                    
                    if pdf_b64:
                        pdf_bytes = base64.b64decode(pdf_b64)
                        st.success("✅ Reporte SBS recuperado")

                        # Botón de Descarga
                        st.download_button(
                            label="📥 DESCARGAR REPORTE COMPLETO (PDF)",
                            data=pdf_bytes,
                            file_name=f"Reporte_SBS_{dni_input}.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )

                        # --- RENDERIZADO COMO IMAGEN ---
                        # Los reportes SBS pueden tener varias páginas, las mostramos todas
                        with st.expander("👁️ Ver Vista Previa del Reporte", expanded=True):
                            images = convert_from_bytes(pdf_bytes, dpi=150)
                            for i, img in enumerate(images):
                                st.image(img, caption=f"Página {i+1}", use_container_width=True)
                    else:
                        st.error("La respuesta no contiene datos PDF.")
                else:
                    st.error(f"Error: {data.get('message', 'No se encontraron registros en SBS')}")
            
            except Exception as e:
                st.error(f"Error de conexión: {e}")

if __name__ == "__main__":
    run()
