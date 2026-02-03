import streamlit as st
import requests

def run():
    st.markdown("<h1 style='text-align: center;'>🎨 Árbol Genealógico Visual Pro</h1>", unsafe_allow_html=True)

    TOKEN = "sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"
    dni_input = st.text_input("Ingrese DNI para generar árbol", max_chars=8, placeholder="45106211")

    if st.button("🖼️ GENERAR ÁRBOL CON FOTOS", use_container_width=True):
        if not dni_input:
            st.warning("Por favor, ingrese un DNI.")
            return

        url = "https://seeker-v6.com/personas/arbol-visualApi"
        headers = {"Authorization": f"Bearer {TOKEN}"}
        params = {"dni": dni_input}

        with st.spinner("Dibujando árbol familiar y cargando fotografías..."):
            try:
                res = requests.get(url, headers=headers, params=params)
                
                if res.status_code == 200:
                    data = res.json()
                    
                    if data.get("status") == "success":
                        # --- CLAVE DEL AJUSTE ---
                        # Usamos la llave 'svg' que confirmamos en la data cruda
                        svg_code = data.get("svg")
                        
                        if svg_code:
                            st.success("✅ Árbol generado con éxito")
                            
                            # Renderizamos el SVG dentro de un contenedor con scroll
                            # El height de 1000px asegura que se vea gran parte del árbol
                            st.components.v1.html(
                                f"""
                                <div style="background-color: white; padding: 20px; border-radius: 10px; overflow: auto;">
                                    {svg_code}
                                </div>
                                """,
                                height=1000,
                                scrolling=True
                            )
                        else:
                            st.error("El servidor no envió el código del gráfico.")
                    else:
                        st.error(f"Error: {data.get('message', 'No se pudo obtener el árbol')}")
                else:
                    st.error(f"Error {res.status_code}: El servidor no responde correctamente.")
                    
            except Exception as e:
                st.error(f"Error de conexión: {e}")

if __name__ == "__main__":
    run()
