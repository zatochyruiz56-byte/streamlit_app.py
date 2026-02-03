import streamlit as st
import requests
import json

def run():
    st.markdown("<h2 style='text-align: center;'>🌳 Árbol Genealógico con Fotos Reales</h2>", unsafe_allow_html=True)

    # Configuración
    TOKEN = "sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"
    
    # --- FUNCIÓN PARA OBTENER FOTO ---
    def get_photo_url(dni):
        # Intentamos el servidor de imágenes de Seeker/Knowlers
        # Si la API de árbol no la da, esta URL suele ser el estándar:
        return f"https://api.reniec.cloud/foto/{dni}" 

    dni_input = st.text_input("DNI a consultar", max_chars=8)

    if st.button("🔍 BUSCAR FAMILIA E IMÁGENES", use_container_width=True):
        try:
            url = "https://seeker-v6.com/personas/arbol-familiar"
            res = requests.get(url, headers={"Authorization": f"Bearer {TOKEN}"}, params={"dni": dni_input})
            
            if res.status_code == 200:
                data = res.json()
                info = data.get("infopersona", {})
                arbol = data.get("arbol", [])

                # --- 1. FICHA DEL TITULAR ---
                st.subheader("🪪 Titular de la Consulta")
                c1, c2 = st.columns([1, 3])
                with c1:
                    # Prioridad: 1. Foto de API, 2. Foto por DNI, 3. Avatar
                    foto_titular = info.get("foto") or get_photo_url(info.get("dni"))
                    st.image(foto_titular, use_container_width=True)
                with c2:
                    st.markdown(f"### {info.get('nombre_completo')}")
                    st.write(f"**DNI:** {info.get('dni')} | **Edad:** {info.get('edad')}")
                    st.write(f"📍 {info.get('ubicacion_completa')}")

                st.divider()

                # --- 2. EL ÁRBOL CON FOTOS ---
                st.subheader("👥 Familiares Directos e Indirectos")
                
                # Agrupamos por tipo para ordenarlos
                grupos = ["PADRE", "MADRE", "HERMANO", "HERMANA", "HIJO", "HIJA", "SOBRINO", "SOBRINA", "CUÑADO", "CUÑADA"]
                
                for grupo in grupos:
                    miembros = [f for f in arbol if f['TIPO'] == grupo]
                    if miembros:
                        st.markdown(f"#### 📍 {grupo}S")
                        # Creamos una cuadrícula de 3 columnas para las fotos de los familiares
                        cols = st.columns(3)
                        for idx, m in enumerate(miembros):
                            with cols[idx % 3]:
                                # Generamos la foto para cada familiar usando su DNI del JSON
                                foto_fam = get_photo_url(m['DNI'])
                                st.image(foto_fam, caption=f"{m['NOMBRES']}", width=120)
                                st.caption(f"🆔 {m['DNI']} ({m['EDAD']} años)")
                                st.markdown("---")
            else:
                st.error("Servidor fuera de línea.")
        except Exception as e:
            st.error(f"Error: {e}")

if __name__ == "__main__":
    run()
