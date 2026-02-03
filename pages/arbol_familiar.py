import streamlit as st
import requests
import json

def run():
    st.set_page_config(layout="wide", page_title="Genealogía Pro")
    
    st.markdown("<h1 style='text-align: center; color: #1E293B;'>🌳 Árbol Familiar Integrado</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Identificación Bio-Genealógica con Verificación de Estado</p>", unsafe_allow_html=True)

    TOKEN = "sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"

    # --- FUNCIÓN DE RECUPERACIÓN DE IMAGEN ---
    def get_photo(dni):
        # Se genera la URL directa del servidor de imágenes de RENIEC
        return f"https://api.reniec.cloud/foto/{dni}"

    dni_input = st.text_input("DNI del Titular", max_chars=8, placeholder="Ejm: 45106211")

    if st.button("🔍 GENERAR REPORTE INTEGRAL", use_container_width=True):
        if not dni_input:
            st.warning("Ingrese un DNI válido.")
            return

        try:
            url = "https://seeker-v6.com/personas/arbol-familiar"
            res = requests.get(url, headers={"Authorization": f"Bearer {TOKEN}"}, params={"dni": dni_input})
            
            if res.status_code == 200:
                data = res.json()
                if data.get("status") == "success":
                    info = data.get("infopersona", {})
                    arbol = data.get("arbol", [])

                    # --- SECCIÓN 1: CABECERA DEL TITULAR ---
                    with st.container(border=True):
                        c1, c2 = st.columns([1, 4])
                        with c1:
                            st.image(get_photo(info['dni']), width=150)
                        with c2:
                            st.subheader(f"👤 {info.get('nombre_completo')}")
                            col_a, col_b, col_c = st.columns(3)
                            col_a.write(f"**DNI:** {info.get('dni')}")
                            col_a.write(f"**Edad:** {info.get('edad')} años")
                            col_b.write(f"**Estado Civil:** {info.get('estado_civil')}")
                            col_b.write(f"**Nacimiento:** {info.get('fecha_nacimiento')}")
                            col_c.write(f"📍 **Ubicación:** {info.get('ubicacion_completa')}")

                    st.markdown("---")

                    # --- SECCIÓN 2: EL ÁRBOL CON LÓGICA DE FALLECIDOS ---
                    st.subheader("👥 Estructura Familiar y Estado Vital")
                    
                    # Definimos las categorías jerárquicas
                    categorias = ["PADRE", "MADRE", "HERMANO", "HERMANA", "HIJO", "HIJA", "SOBRINO", "SOBRINA", "CUÑADO", "CUÑADA"]

                    for cat in categorias:
                        # Filtramos miembros por tipo
                        miembros = [m for m in arbol if cat in m['TIPO']]
                        
                        if miembros:
                            st.markdown(f"#### 📍 {cat}S")
                            cols = st.columns(5) # Formato rejilla de fotos
                            
                            for i, m in enumerate(miembros):
                                with cols[i % 5]:
                                    # LÓGICA DE FALLECIDOS:
                                    # Si la edad es muy alta (ejm > 95) o la API lo indica, marcamos alerta
                                    es_fallecido = int(m['EDAD']) > 90 
                                    
                                    # Aplicamos filtro visual si es probable fallecido
                                    if es_fallecido:
                                        st.image(get_photo(m['DNI']), width=110, use_container_width=False)
                                        st.markdown(f"<p style='color:red; font-size:12px; font-weight:bold; margin-top:-10px;'>✟ POSIBLE FALLECIDO</p>", unsafe_allow_html=True)
                                    else:
                                        st.image(get_photo(m['DNI']), width=110)
                                    
                                    st.write(f"**{m['NOMBRES']}**")
                                    st.caption(f"🆔 {m['DNI']} | 🎂 {m['EDAD']} años")
                            st.markdown("---")
                else:
                    st.error("No se encontraron resultados.")
            else:
                st.error(f"Error {response.status_code}: Servidor inestable.")
        except Exception as e:
            st.error(f"Error de conexión: {e}")

if __name__ == "__main__":
    run()
