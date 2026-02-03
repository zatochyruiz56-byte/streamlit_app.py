import streamlit as st
import requests
import base64

def run():
    st.markdown("<h1 style='text-align: center;'>🪪 Ficha RENIEC Oficial</h1>", unsafe_allow_html=True)

    TOKEN = "sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"
    dni_input = st.text_input("Ingrese DNI para obtener ficha", max_chars=8)

    if st.button("📄 OBTENER FICHA ORIGINAL", use_container_width=True):
        if not dni_input:
            st.warning("Ingrese un DNI.")
            return

        url = "https://seeker-v6.com/personas/api/ficha"
        headers = {"Authorization": f"Bearer {TOKEN}"}
        payload = {"dni": dni_input}

        with st.spinner("Procesando PDF oficial..."):
            try:
                res = requests.post(url, headers=headers, json=payload)
                
                if res.status_code == 200:
                    data = res.json()
                    
                    if data.get("status") == "success":
                        pdf_b64 = data.get("pdf")
                        
                        if pdf_b64:
                            # 1. Decodificamos a bytes para la descarga
                            pdf_bytes = base64.b64decode(pdf_b64)
                            
                            st.success("✅ Ficha cargada correctamente")

                            # Botón de Descarga (Este ya te funcionaba bien)
                            st.download_button(
                                label="📥 DESCARGAR ARCHIVO PDF",
                                data=pdf_bytes,
                                file_name=f"Ficha_RENIEC_{dni_input}.pdf",
                                mime="application/pdf",
                                use_container_width=True
                            )

                            # 2. SOLUCIÓN AL ERROR DE BLOQUEO:
                            # En lugar de un iframe, usamos un visor de PDF embebido 
                            # con una técnica de 'object data' que es más amigable con Chrome
                            pdf_display = f"""
                                <object data="data:application/pdf;base64,{pdf_b64}" width="100%" height="800" type="application/pdf">
                                    <div style="padding:20px; text-align:center; background:#f8d7da; color:#721c24; border-radius:10px;">
                                        ⚠️ Tu navegador no permite la vista previa automática. 
                                        <br>Usa el botón de arriba para descargar y ver el documento.
                                    </div>
                                </object>
                            """
                            st.markdown(pdf_display, unsafe_allow_html=True)
                        else:
                            st.error("La respuesta no contiene un archivo PDF.")
                    else:
                        st.error(f"Error: {data.get('message', 'DNI no encontrado')}")
                else:
                    st.error("Error de conexión con el servidor de RENIEC.")
                    
            except Exception as e:
                st.error(f"Error técnico: {e}")

if __name__ == "__main__":
    run()
