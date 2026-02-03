import streamlit as st
import requests
import base64
from pdf2image import convert_from_bytes

def run():
    st.markdown("<h1 style='text-align: center;'>🏦 Reporte de Deudas SBS</h1>", unsafe_allow_html=True)

    TOKEN = "sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"
    dni_input = st.text_input("Ingrese DNI para consulta SBS", max_chars=8)

    if st.button("📊 GENERAR REPORTE SBS", use_container_width=True):
        if not dni_input:
            st.warning("Ingrese un DNI.")
            return

        url = "https://seeker-v6.com/personas/sbs_pdf_api"
        headers = {"Authorization": f"Bearer {TOKEN}"}
        payload = {"dni": dni_input}

        with st.spinner("Consultando SBS (esto puede demorar hasta 30 segundos)..."):
            try:
                # Aumentamos el timeout porque los PDF de SBS son pesados
                res = requests.post(url, headers=headers, json=payload, timeout=45)
                
                # Verificamos si la respuesta es realmente un JSON
                if res.status_code == 200:
                    try:
                        data = res.json()
                    except:
                        st.error("El servidor respondió algo que no es JSON. Posible mantenimiento.")
                        st.code(res.text[:500]) # Mostramos el inicio del error
                        return

                    if data.get("status") == "success":
                        # En SBS el PDF suele venir directo en la raíz o en 'data'
                        pdf_b64 = data.get("pdf") or data.get("data", {}).get("pdf")
                        
                        if pdf_b64:
                            pdf_bytes = base64.b64decode(pdf_b64)
                            st.success("✅ Reporte recuperado con éxito")

                            st.download_button(
                                label="📥 DESCARGAR REPORTE PDF",
                                data=pdf_bytes,
                                file_name=f"SBS_{dni_input}.pdf",
                                mime="application/pdf",
                                use_container_width=True
                            )

                            # Visualización segura
                            images = convert_from_bytes(pdf_bytes, dpi=120)
                            for i, img in enumerate(images):
                                st.image(img, caption=f"Página {i+1}", use_container_width=True)
                        else:
                            st.error("No se encontró la cadena PDF en la respuesta.")
                            st.json(data) # Mostramos qué llegó para investigar
                    else:
                        st.error(f"API Error: {data.get('message', 'DNI no encontrado o sin historial')}")
                else:
                    st.error(f"Error del servidor (Código {res.status_code})")
                    st.info("Esto puede pasar si el servicio de la SBS está caído temporalmente.")

            except requests.exceptions.Timeout:
                st.error("⏳ Tiempo de espera agotado. La SBS está demorando demasiado.")
            except Exception as e:
                st.error(f"Error inesperado: {str(e)}")

if __name__ == "__main__":
    run()
