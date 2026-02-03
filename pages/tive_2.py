import streamlit as st
import requests
import base64

def run():
    st.markdown("<h1 style='text-align: center;'>🚗 Tarjeta Vehicular TIVE V2</h1>", unsafe_allow_html=True)

    TOKEN = "sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"
    placa_input = st.text_input("Ingrese Placa del Vehículo", max_chars=6, placeholder="ABC123").upper()

    if st.button("🔍 CONSULTAR TIVE V2", use_container_width=True):
        if not placa_input:
            st.warning("Por favor, ingrese una placa válida.")
            return

        # URL oficial del endpoint
        url = "https://seeker-v6.com/vehiculos/api_tive_v2"
        headers = {"Authorization": f"Bearer {TOKEN}"}
        payload = {"placa": placa_input}

        with st.spinner("Buscando registro vehicular..."):
            try:
                # Usamos un timeout de 45 segundos para procesos pesados
                res = requests.post(url, headers=headers, json=payload, timeout=45)
                
                # Validación de seguridad: Si responde HTML, el servicio está en mantenimiento
                if "text/html" in res.headers.get("Content-Type", ""):
                    st.error("❌ El servicio TIVE no está disponible actualmente (Error de Sesión).")
                    return

                data = res.json()

                if data.get("status") == "success":
                    st.success(f"✅ Datos obtenidos. Créditos restantes: {data.get('creditos_restantes')}")
                    
                    # TIVE V2 suele devolver un PDF o imágenes en base64 dentro de 'data'
                    info_tive = data.get("data", {})
                    archivo_b64 = info_tive.get("pdf") or info_tive.get("base64")

                    if archivo_b64:
                        file_bytes = base64.b64decode(archivo_b64)
                        
                        # Botón para descargar el documento oficial
                        st.download_button(
                            label="📥 DESCARGAR TIVE (PDF)",
                            data=file_bytes,
                            file_name=f"TIVE_{placa_input}.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )

                        # Intentar mostrar vista previa
                        try:
                            from pdf2image import convert_from_bytes
                            images = convert_from_bytes(file_bytes, dpi=150)
                            for i, img in enumerate(images):
                                st.image(img, caption=f"Página {i+1}", use_container_width=True)
                        except Exception:
                            st.info("💡 Documento generado. Use el botón de descarga para visualizarlo.")
                    else:
                        st.warning("La consulta fue exitosa pero no se encontró un archivo visualizable.")
                        st.json(info_tive)
                else:
                    st.error(f"Error: {data.get('message', 'No se encontró la placa')}")

            except Exception as e:
                st.error(f"Fallo técnico al conectar con Seeker: {str(e)}")

if __name__ == "__main__":
    run()
