import streamlit as st
import requests
import base64
from pdf2image import convert_from_bytes

def run():
    st.markdown("<h1 style='text-align: center;'>🎴 Generador de DNI Virtual</h1>", unsafe_allow_html=True)

    TOKEN = "sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"
    
    col1, col2 = st.columns(2)
    with col1:
        dni_input = st.text_input("DNI de 8 dígitos", max_chars=8, placeholder="45106211")
    with col2:
        # Ajustamos los nombres para que coincidan exactamente con lo que la API espera
        tipo_display = st.selectbox("Tipo de Documento", ["DNI AZUL", "DNI ELECTRÓNICO"])
        
    # Mapeo de nombres amigables a valores de API
    dict_tipos = {
        "DNI AZUL": "azul",
        "DNI ELECTRÓNICO": "electronico"
    }
    valor_api = dict_tipos[tipo_display]

    if st.button("🚀 GENERAR DNI VIRTUAL", use_container_width=True):
        if not dni_input:
            st.warning("Por favor, ingrese un DNI.")
            return

        url = "https://seeker-v6.com/personas/virtualdni"
        headers = {"Authorization": f"Bearer {TOKEN}"}
        payload = {"dni": dni_input, "tipo": valor_api}

        with st.spinner("Conectando con el servidor de diseño..."):
            try:
                # Importante: La documentación muestra que es un POST
                res = requests.post(url, headers=headers, json=payload)
                data = res.json()

                if data.get("status") == "success":
                    pdf_b64 = data.get("pdf")
                    pdf_bytes = base64.b64decode(pdf_b64)

                    st.success(f"✅ {tipo_display} generado correctamente")

                    # Botón de Descarga
                    st.download_button(
                        label="📥 DESCARGAR PDF PARA IMPRIMIR",
                        data=pdf_bytes,
                        file_name=f"DNI_Virtual_{dni_input}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )

                    # --- VISUALIZACIÓN POR IMAGEN (Anti-Bloqueo) ---
                    # Convertimos el PDF a imagen para que se vea sin errores
                    images = convert_from_bytes(pdf_bytes, dpi=200)
                    
                    for i, img in enumerate(images):
                        label = "PARTE FRONTAL" if i == 0 else "PARTE POSTERIOR"
                        st.image(img, caption=label, use_container_width=True)
                
                else:
                    # Aquí capturamos el error exacto que te salía
                    st.error(f"Error de la API: {data.get('message', 'Parámetros incorrectos')}")
            
            except Exception as e:
                st.error(f"Error técnico: {e}")

if __name__ == "__main__":
    run()
