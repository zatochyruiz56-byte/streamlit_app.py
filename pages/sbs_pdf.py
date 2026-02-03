import streamlit as st
import requests
import base64
from pdf2image import convert_from_bytes

def run():
    st.title("🏦 Reporte de Deudas SBS (Rescate)")

    TOKEN = "sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"
    dni_input = st.text_input("DNI para reporte", max_chars=8)

    if st.button("📊 GENERAR REPORTE"):
        url = "https://seeker-v6.com/personas/sbs_pdf_api"
        
        # Usamos una sesión para mayor estabilidad
        session = requests.Session()
        headers = {
            "Authorization": f"Bearer {TOKEN}",
            "Accept": "application/json"
        }
        payload = {"dni": dni_input}

        with st.spinner("⏳ Procesando reporte pesado... Por favor no cierres la pestaña."):
            try:
                # El timeout de 60s es vital para que no se corte la descarga
                response = session.post(url, headers=headers, json=payload, timeout=60)
                
                # Si recibimos HTML (Login), detenemos el proceso antes de que de error de JSON
                if "text/html" in response.headers.get("Content-Type", ""):
                    st.error("❌ El servidor intentó redirigirte al Login. Reintenta en 1 minuto.")
                    with st.expander("Ver respuesta del servidor"):
                        st.code(response.text[:1000])
                    return

                data = response.json()
                
                if data.get("status") == "success":
                    # Intentamos obtener el PDF de cualquier ubicación posible en el JSON
                    pdf_b64 = data.get("pdf") or data.get("data", {}).get("pdf")
                    
                    if pdf_b64:
                        pdf_bytes = base64.b64decode(pdf_b64)
                        st.success("✅ ¡Reporte rescatado!")

                        # Visualización en imágenes para que Chrome no bloquee
                        images = convert_from_bytes(pdf_bytes, dpi=120)
                        for i, img in enumerate(images):
                            st.image(img, caption=f"Página {i+1}", use_container_width=True)
                        
                        st.download_button("📥 Descargar Reporte Completo", pdf_bytes, f"SBS_{dni_input}.pdf")
                else:
                    st.error(f"Error: {data.get('message')}")

            except Exception as e:
                st.error(f"Error técnico: {str(e)}")

if __name__ == "__main__":
    run()
