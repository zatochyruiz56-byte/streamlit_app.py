import streamlit as st
import requests
import base64
from pdf2image import convert_from_bytes
import io

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

        with st.spinner("Generando reporte oficial de deudas..."):
            try:
                res = requests.post(url, headers=headers, json=payload, timeout=60)
                
                if res.status_code == 200:
                    try:
                        data = res.json()
                    except:
                        st.error("Error: La respuesta no es un formato válido.")
                        return

                    if data.get("status") == "success":
                        # Buscamos el PDF en ambas ubicaciones posibles
                        pdf_b64 = data.get("pdf") or data.get("data", {}).get("pdf")
                        
                        if pdf_b64:
                            pdf_bytes = base64.b64decode(pdf_b64)
                            
                            # --- MEJORA DE FORMATO Y DESCARGA ---
                            st.success("✅ Reporte generado correctamente")
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                st.download_button(
                                    label="📥 DESCARGAR PDF ORIGINAL",
                                    data=pdf_bytes,
                                    file_name=f"SBS_{dni_input}.pdf",
                                    mime="application/pdf",
                                    use_container_width=True
                                )
                            with col2:
                                # Opción extra por si quieren imprimir directo
                                st.info("💡 El PDF original mantiene el formato oficial A4.")

                            # --- VISUALIZACIÓN DE ALTA CALIDAD ---
                            # Subimos el DPI a 200 para que las letras pequeñas de la SBS se lean
                            images = convert_from_bytes(pdf_bytes, dpi=200)
                            
                            st.markdown("---")
                            st.subheader("👁️ Vista Previa del Documento")
                            
                            for i, img in enumerate(images):
                                # Usamos un expander para no ocupar tanto espacio si son muchas páginas
                                with st.expander(f"Página {i+1} del Reporte", expanded=True if i==0 else False):
                                    st.image(img, use_container_width=True)
                        else:
                            st.error("No se encontró el contenido del PDF.")
                    else:
                        st.error(f"Error de API: {data.get('message')}")
                else:
                    st.error(f"Servidor fuera de línea (Código {res.status_code})")

            except Exception as e:
                st.error(f"Error de visualización: {str(e)}")

if __name__ == "__main__":
    run()
