import streamlit as st
import requests

def run():
    st.set_page_config(layout="wide")
    st.markdown("<h1 style='text-align: center;'>🧬 Genealogía Visual Premium</h1>", unsafe_allow_html=True)

    TOKEN = "sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"
    
    # --- MOTOR DE IMÁGENES ---
    # Esta función construye la URL de la imagen basándose en el DNI detectado
    def get_photo(dni):
        # Intentamos el servidor de caché de imágenes (ajusta la URL según tu proveedor)
        return f"https://api.reniec.cloud/foto/{dni}"

    dni_input = st.text_input("DNI del Titular", max_chars=8)

    if st.button("🔍 GENERAR ÁRBOL CON FOTOS", use_container_width=True):
        url = "https://seeker-v6.com/personas/arbol-familiar"
        try:
            res = requests.get(url, headers={"Authorization": f"Bearer {TOKEN}"}, params={"dni": dni_input})
            data = res.json()

            if data.get("status") == "success":
                info = data.get("infopersona", {})
                arbol = data.get("arbol", [])

                # --- SECCIÓN TITULAR ---
                st.subheader("👤 Datos del Titular")
                c1, c2, c3 = st.columns([1, 2, 2])
                with c1:
                    st.image(get_photo(info['dni']), caption="FOTO TITULAR", width=160)
                with c2:
                    st.write(f"**Nombre:** {info['nombre_completo']}")
                    st.write(f"**DNI:** {info['dni']}")
                    st.write(f"**Edad:** {info['edad']} años")
                with c3:
                    st.write(f"**Estado Civil:** {info['estado_civil']}")
                    st.write(f"**Dirección:** {info['direccion']}")

                st.divider()

                # --- SECCIÓN ÁRBOL GENEALÓGICO ---
                st.subheader("👥 Vínculos Familiares con Registro Fotográfico")
                
                # Clasificamos para mostrar en orden jerárquico
                categorias = ["PADRE", "MADRE", "HERMANO", "HERMANA", "HIJO", "HIJA", "SOBRINO", "SOBRINA"]
                
                for cat in categorias:
                    miembros = [m for m in arbol if cat in m['TIPO']]
                    if miembros:
                        st.markdown(f"#### {cat}S")
                        # Creamos una fila de fotos para cada categoría
                        cols = st.columns(5) 
                        for i, m in enumerate(miembros):
                            with cols[i % 5]:
                                st.image(get_photo(m['DNI']), width=120)
                                st.caption(f"**{m['NOMBRES']}**")
                                st.caption(f"🆔 {m['DNI']}")
                        st.markdown("---")
            else:
                st.error("DNI no encontrado o error de API.")
        except Exception as e:
            st.error(f"Error técnico: {e}")

if __name__ == "__main__":
    run()
