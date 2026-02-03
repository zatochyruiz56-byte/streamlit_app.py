import streamlit as st
import requests
import base64

def run():
    st.markdown("<h1 style='text-align: center;'>🪪 Ficha RENIEC Oficial</h1>", unsafe_allow_html=True)

    TOKEN = "sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"
    dni_input = st.text_input("Ingrese DNI para obtener PDF", max_chars=8)

    if st.button("📄 OBTENER FICHA ORIGINAL", use_container_width=True):
        if not dni_input:
            st.warning("Ingrese un DNI.")
            return

        url = "https://seeker-v6.com/personas/api/ficha"
        headers = {"Authorization": f"Bearer {TOKEN}"}
        payload = {"dni": dni_input}

        with st.spinner("Descargando y procesando documento..."):
            try:
                # Usamos POST como indica tu documentación
                res = requests.post(url, headers=headers, json=payload)
                
                if res.status_code == 200:
                    data = res.json()
                    
                    if data.get("status") == "success":
                        # Extraemos la cadena base64 del PDF
                        pdf_b64 = data.get("pdf")
                        
                        if pdf_b64:
                            # 1. Preparar la descarga del archivo real
                            pdf_bytes = base64.b64decode(pdf_b64)
                            
                            st.success("✅ Ficha recuperada con éxito")

                            # Botón de descarga para PDF Real
                            st.download_button(
                                label="📥 DESCARGAR FICHA EN PDF",
                                data=pdf_bytes,
                                file_name=f"Ficha_RENIEC_{dni_input}.pdf",
                                mime="application/pdf",
                                use_container_width=True
                            )

                            # 2. Visualización previa en la App
                            # Creamos un iframe para ver el PDF sin salir de Streamlit
                            pdf_display = f'<iframe src="data:application/pdf;base64,{pdf_b64}" width="100%" height="800" type="application/pdf"></iframe>'
                            st.markdown(pdf_display, unsafe_allow_html=True)
                        else:
                            st.error("El servidor no incluyó el archivo PDF en la respuesta.")
                    else:
                        st.error(f"Error: {data.get('message', 'No se pudo generar la ficha')}")
                else:
                    st.error(f"Error del servidor: {res.status_code}")
                    
            except Exception as e:
                st.error(f"Error técnico: {e}")

if __name__ == "__main__":
    run()
