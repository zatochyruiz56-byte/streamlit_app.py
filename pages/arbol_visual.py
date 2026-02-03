import streamlit as st
import requests

def run():
    st.markdown("<h1 style='text-align: center;'>🛠️ Debug: Árbol Visual (Data Cruda)</h1>", unsafe_allow_html=True)

    TOKEN = "sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"
    dni_input = st.text_input("Ingrese DNI para inspección de datos", max_chars=8)

    if st.button("📡 OBTENER RESPUESTA CRUDA"):
        if not dni_input:
            st.warning("Ingrese un DNI.")
            return

        url = "https://seeker-v6.com/personas/arbol-visualApi"
        headers = {"Authorization": f"Bearer {TOKEN}"}
        params = {"dni": dni_input}

        with st.spinner("Consultando servidor..."):
            try:
                res = requests.get(url, headers=headers, params=params)
                
                # Mostramos el Código de Estado HTTP
                st.info(f"Código de Respuesta del Servidor: {res.status_code}")

                if res.status_code == 200:
                    try:
                        # Intentamos mostrarlo como JSON formateado
                        raw_data = res.json()
                        st.subheader("📦 JSON Recibido:")
                        st.json(raw_data)
                        
                        # Si el SVG está en el campo 'data', lo mostramos como texto plano para inspeccionarlo
                        if "data" in raw_data:
                            st.subheader("📝 Contenido del campo 'data' (Primeros 500 caracteres):")
                            st.text(str(raw_data["data"])[:500] + "...")
                            
                    except Exception:
                        # Si no es JSON, mostramos el texto plano (posiblemente el SVG directo)
                        st.subheader("📄 Texto Plano Recibido:")
                        st.code(res.text, language="xml")
                else:
                    st.error(f"Error del Servidor: {res.text}")
                    
            except Exception as e:
                st.error(f"Error de conexión: {e}")

if __name__ == "__main__":
    run()
