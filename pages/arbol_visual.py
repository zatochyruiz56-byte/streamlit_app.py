import streamlit as st
import requests
import base64

def run():
    st.markdown("<h1 style='text-align: center;'>🎨 Árbol Genealógico Visual (Fotos)</h1>", unsafe_allow_html=True)

    TOKEN = "sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"
    dni_input = st.text_input("Ingrese DNI para generar árbol visual", max_chars=8)

    if st.button("🖼️ GENERAR ÁRBOL GRÁFICO", use_container_width=True):
        if not dni_input:
            st.warning("Por favor, ingrese un DNI.")
            return

        with st.spinner("Generando estructura visual con imágenes..."):
            url = "https://seeker-v6.com/personas/arbol-visualApi"
            headers = {"Authorization": f"Bearer {TOKEN}"}
            params = {"dni": dni_input}

            try:
                res = requests.get(url, headers=headers, params=params)
                
                if res.status_code == 200:
                    data = res.json()
                    
                    if data.get("status") == "success":
                        # El campo 'data' suele contener el código SVG o una URL al gráfico
                        # Si es un SVG directo, lo mostramos así:
                        svg_content = data.get("data")
                        
                        st.success("Árbol visual generado correctamente")
                        
                        # Renderizado del SVG para que se vean las fotos y conexiones
                        st.components.v1.html(
                            f'<div style="display:flex; justify-content:center;">{svg_content}</div>',
                            height=800,
                            scrolling=True
                        )
                    else:
                        st.error(f"Error de API: {data.get('message', 'No se pudo generar el visual')}")
                else:
                    st.error(f"Error de conexión: Código {res.status_code}")
                    
            except Exception as e:
                st.error(f"Error técnico al procesar el visual: {e}")

if __name__ == "__main__":
    run()
