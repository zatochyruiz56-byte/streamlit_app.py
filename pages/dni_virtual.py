import streamlit as st
import requests
import base64
from io import BytesIO
from PIL import Image

def run():
    st.markdown("<h1 style='text-align: center;'>🎴 Generador de DNI Virtual</h1>", unsafe_allow_html=True)

    TOKEN = "sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"
    
    col1, col2 = st.columns(2)
    with col1:
        dni_input = st.text_input("DNI de 8 dígitos", max_chars=8, placeholder="60799566")
    with col2:
        # Usamos los valores exactos que la API aceptó en el diagnóstico
        tipo_display = st.selectbox("Tipo de Documento", ["AZUL", "ELECTRONICO"])

    if st.button("🚀 GENERAR DNI VIRTUAL", use_container_width=True):
        if not dni_input:
            st.warning("Por favor, ingrese un DNI.")
            return

        url = "https://seeker-v6.com/personas/virtualdni"
        headers = {"Authorization": f"Bearer {TOKEN}"}
        payload = {
            "dni": dni_input,
            "tipo": tipo_display  # Enviamos el valor en MAYÚSCULAS
        }

        with st.spinner("Recuperando imágenes de identidad..."):
            try:
                res = requests.post(url, headers=headers, json=payload)
                data = res.json()

                if data.get("status") == "success":
                    # La info real está dentro de la llave 'data'
                    info_dni = data.get("data", {})
                    frontal_b64 = info_dni.get("frontal_base64")
                    posterior_b64 = info_dni.get("posterior_base64")

                    if frontal_b64 and posterior_b64:
                        st.success(f"✅ DNI {tipo_display} generado con éxito")

                        # --- MOSTRAR LAS IMÁGENES ---
                        col_a, col_b = st.columns(2)
                        
                        with col_a:
                            st.image(f"data:image/jpeg;base64,{frontal_b64}", caption="ANVERSO", use_container_width=True)
                        
                        with col_b:
                            st.image(f"data:image/jpeg;base64,{posterior_b64}", caption="REVERSO", use_container_width=True)

                        # --- OPCIÓN DE DESCARGA ---
                        # Para descargar, podemos dar la opción de bajar la imagen frontal
                        st.download_button(
                            label="📥 DESCARGAR ANVERSO (JPG)",
                            data=base64.b64decode(frontal_b64),
                            file_name=f"DNI_{dni_input}_frontal.jpg",
                            mime="image/jpeg"
                        )
                    else:
                        st.error("No se recibieron las imágenes del DNI.")
                else:
                    st.error(f"Error de la API: {data.get('message', 'Tipo no válido')}")
            
            except Exception as e:
                st.error(f"Fallo en la conexión: {e}")

if __name__ == "__main__":
    run()
