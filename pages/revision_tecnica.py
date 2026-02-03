import streamlit as st
import requests

def run():
    st.markdown("<h1 style='text-align: center;'>🔍 Revisión Técnica Vehicular</h1>", unsafe_allow_html=True)

    TOKEN = "sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"
    placa_input = st.text_input("Ingrese Placa (ej: ABC123)", max_chars=7).upper()

    if st.button("📊 CONSULTAR REVISIÓN", use_container_width=True):
        if not placa_input:
            st.warning("Por favor, ingrese una placa.")
            return

        # Endpoint según documentación (Método GET)
        url = "https://seeker-v6.com/vehiculos/revision_tecnica"
        headers = {"Authorization": f"Bearer {TOKEN}"}
        params = {"placa": placa_input}

        with st.spinner("Verificando estado de revisión técnica..."):
            try:
                # Al ser GET, pasamos los datos en 'params'
                res = requests.get(url, headers=headers, params=params, timeout=20)
                
                # Verificación de "Error de Sesión" persistente
                if "text/html" in res.headers.get("Content-Type", ""):
                    st.error("🚨 El servidor de Seeker sigue redirigiendo al Login.")
                    with st.expander("Ver respuesta del servidor"):
                        st.code(res.text[:500])
                    return

                data = res.json()

                if data.get("status") == "success":
                    st.success(f"✅ Consulta exitosa. Créditos restantes: {data.get('creditos_restantes')}")
                    
                    info = data.get("data", {})
                    if info:
                        # Mostramos los datos clave encontrados en la respuesta JSON
                        st.subheader("📋 Resultados de la Inspección")
                        st.write(f"**Resultado:** {info.get('resultado', 'N/A')}")
                        st.write(f"**Vigencia hasta:** {info.get('vigencia', 'N/A')}")
                        st.write(f"**Planta:** {info.get('planta', 'N/A')}")
                        st.write(f"**Certificado:** {info.get('certificado', 'N/A')}")
                        
                        with st.expander("Ver JSON completo"):
                            st.json(info)
                    else:
                        st.info("No se encontraron registros de revisión para esta placa.")
                else:
                    st.error(f"Error: {data.get('message', 'Error desconocido')}")

            except Exception as e:
                st.error(f"Fallo de conexión técnica: {str(e)}")

if __name__ == "__main__":
    run()
