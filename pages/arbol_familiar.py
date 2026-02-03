import streamlit as st
import requests
import json

def run():
    st.markdown("<h2 style='text-align: center; color: #1E293B;'>🌳 Consulta de Árbol Familiar Premium</h2>", unsafe_allow_html=True)
    st.markdown("---")

    API_URL = "https://seeker-v6.com/personas/arbol-familiar"
    TOKEN = "sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"

    dni = st.text_input("Ingrese DNI para búsqueda genealógica", max_chars=8, placeholder="Ejm: 12345678")

    if st.button("🚀 GENERAR REPORTE COMPLETO", use_container_width=True):
        if not dni:
            st.warning("Debe ingresar un DNI.")
            return

        try:
            with st.spinner("Extrayendo registros e imágenes..."):
                response = requests.get(API_URL, headers={"Authorization": f"Bearer {TOKEN}"}, params={"dni": dni})
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get("status") == "success":
                    info = data.get("infopersona", {})
                    familia = data.get("arbol", [])

                    # --- SECCIÓN 1: DATOS DEL TITULAR + FOTO ---
                    st.subheader("🪪 Ficha de Identidad")
                    col_img, col_txt = st.columns([1, 2])

                    with col_img:
                        # LÓGICA DE FOTO: Si el API devuelve Base64 o URL, se muestra. 
                        # Si es null, intentamos la ruta estándar de Seeker para fotos
                        foto_data = info.get("foto")
                        if foto_data:
                            st.image(foto_data, caption=f"FOTO RENIEC - {info.get('dni')}", use_container_width=True)
                        else:
                            # Placeholder profesional si no hay imagen
                            st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=180)
                            st.caption("⚠️ Imagen no disponible en este registro")

                    with col_txt:
                        st.markdown(f"### {info.get('nombre_completo')}")
                        
                        # Tabla de datos rápida
                        datos_tabla = {
                            "DNI": info.get("dni"),
                            "Edad": f"{info.get('edad')} años",
                            "Estado Civil": info.get("estado_civil"),
                            "Fecha Nac.": info.get("fecha_nacimiento"),
                            "Ubicación": info.get("ubicacion_completa"),
                            "Dirección": info.get("direccion")
                        }
                        st.table([datos_tabla])

                    st.markdown("---")

                    # --- SECCIÓN 2: DESGLOSE DEL ÁRBOL FAMILIAR ---
                    st.subheader("👥 Vínculos Familiares Encontrados")
                    
                    # Usamos Tabs para no saturar la pantalla
                    tab_padres, tab_hermanos, tab_sobrinos, tab_otros = st.tabs([
                        "👴 Padres", "👦 Hermanos", "👶 Sobrinos", "🤝 Otros Vínculos"
                    ])

                    with tab_padres:
                        padres = [f for f in familia if f['TIPO'] in ['PADRE', 'MADRE']]
                        for p in padres:
                            with st.expander(f"📌 {p['TIPO']}: {p['NOMBRES']} {p['APELLIDOS']}", expanded=True):
                                col_a, col_b = st.columns(2)
                                col_a.write(f"**DNI:** {p['DNI']}")
                                col_a.write(f"**Edad:** {p['EDAD']} años")
                                col_b.write(f"**Género:** {p['GENERO']}")
                                col_b.write(f"**Verificación:** {p['VERIFICACION']}")

                    with tab_hermanos:
                        hermanos = [f for f in familia if 'HERMANO' in f['TIPO']]
                        for h in hermanos:
                            st.info(f"**{h['TIPO']}:** {h['NOMBRES']} {h['APELLIDOS']} | DNI: `{h['DNI']}` | {h['EDAD']} años")

                    with tab_sobrinos:
                        sobrinos = [f for f in familia if 'SOBRIN' in f['TIPO']]
                        if sobrinos:
                            for s in sobrinos:
                                st.success(f"🔹 **{s['TIPO']}:** {s['NOMBRES']} {s['APELLIDOS']} (DNI: {s['DNI']})")
                        else:
                            st.write("No se detectaron sobrinos.")

                    with tab_otros:
                        otros = [f for f in familia if f['TIPO'] in ['CUÑADO', 'CUÑADA']]
                        for o in otros:
                            st.warning(f"🔸 **{o['TIPO']}:** {o['NOMBRES']} {o['APELLIDOS']} | DNI: `{o['DNI']}`")

                else:
                    st.error("No se encontró información para ese DNI.")
            else:
                st.error(f"Error en servidor: {response.status_code}")

        except Exception as e:
            st.error(f"Error de conexión: {e}")

if __name__ == "__main__":
    run()
