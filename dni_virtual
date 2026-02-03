import streamlit as st
import requests
import base64
from pdf2image import convert_from_bytes

def run():
    st.markdown("<h1 style='text-align: center;'>🪪 Generador de DNI Virtual</h1>", unsafe_allow_html=True)

    TOKEN = "sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"
    
    col1, col2 = st.columns(2)
    with col1:
        dni_input = st.text_input("DNI de 8 dígitos", max_chars=8)
    with col2:
        tipo_dni = st.selectbox("Tipo de Documento", ["azul", "electronico"])

    if st.button("🎴 GENERAR DNI VIRTUAL", use_container_width=True):
        if not dni_input:
            st.warning("Por favor, ingrese un DNI.")
            return

        url = "https://seeker-v6.com/personas/virtualdni"
        headers = {"Authorization": f"Bearer {TOKEN}"}
        # Enviamos DNI y el tipo seleccionado
        payload = {"dni": dni_input, "tipo": tipo_dni}

        with st.spinner("Generando réplica de identidad..."):
            try:
                res = requests.post(url, headers=headers, json=payload)
                data = res.json()

                if data.get("status") == "success":
                    pdf_b64 = data.get("pdf")
                    pdf_bytes = base64.b64decode(pdf_b64)

                    st.success(f"✅ DNI Virtual ({tipo_dni.upper()}) generado")

                    # --- RENDERIZADO ANTIBLOQUEO ---
                    # Convertimos las páginas del PDF (anverso y reverso) a imágenes
                    images = convert_from_bytes(pdf_bytes, dpi=200)

                    # Botón de descarga del archivo original
                    st.download_button(
                        label="📥 DESCARGAR DNI (PDF)",
                        data=pdf_bytes,
                        file_name=f"DNI_Virtual_{dni_input}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )

                    # Mostramos las imágenes una al lado de la otra o una debajo de otra
                    for i, img in enumerate(images):
                        label = "ANVERSO (Frontal)" if i == 0 else "REVERSO (Posterior)"
                        st.image(img, caption=label, use_container_width=True)
                
                else:
                    st.error(f"Error: {data.get('message', 'No se pudo generar el documento')}")
            
            except Exception as e:
                st.error(f"Fallo en la conexión: {e}")

if __name__ == "__main__":
    run()
