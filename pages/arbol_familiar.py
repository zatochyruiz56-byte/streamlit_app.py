import streamlit as st
import requests
import json

def run():
    st.title("🌳 Consulta de Árbol Genealógico")
    st.markdown("---")

    # Configuración de API
    API_URL = "https://seeker-v6.com/personas/arbol-familiar"
    TOKEN = "sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"

    dni = st.text_input("Ingrese DNI para expandir árbol", max_chars=8)

    if st.button("🚀 GENERAR CONSULTA COMPLETA", use_container_width=True):
        if not dni:
            st.warning("Por favor, ingrese un DNI.")
            return

        try:
            with st.spinner("Accediendo a registros civiles..."):
                response = requests.get(API_URL, headers={"Authorization": f"Bearer {TOKEN}"}, params={"dni": dni})
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get("status") == "success":
                    info = data.get("infopersona", {})
                    familia = data.get("arbol", [])

                    # --- SECCIÓN 1: FICHA DE IDENTIDAD (Imagen y Texto) ---
                    st.subheader("🪪 Información del Titular")
                    col_foto, col_datos = st.columns([1, 2])

                    with col_foto:
                        # Si la API no envía foto, usamos un avatar por defecto
                        foto_url = info.get("foto") if info.get("foto") else "https://cdn-icons-png.flaticon.com/512/3135/3135715.png"
                        st.image(foto_url, caption=f"DNI: {info.get('dni')}", width=200)
                        st.metric("Estado Civil", info.get("estado_civil", "N/A"))

                    with col_datos:
                        st.markdown(f"### {info.get('nombre_completo')}")
                        st.write(f"📅 **Nacimiento:** {info.get('fecha_nacimiento')} ({info.get('edad')} años)")
                        st.write(f"📍 **Ubicación:** {info.get('ubicacion_completa')}")
                        st.write(f"🏠 **Dirección:** {info.get('direccion')}")
                        st.write(f"🛡️ **Inscripción:** {info.get('fecha_inscripcion')}")

                    st.markdown("---")

                    # --- SECCIÓN 2: VÍNCULOS DETECTADOS (Filtro Inteligente) ---
                    st.subheader("👥 Vínculos Familiares Detectados")
                    
                    # Clasificamos la lista 'arbol' según el campo 'TIPO'
                    t1, t2, t3, t4 = st.tabs(["Padres", "Hermanos", "Sobrinos", "Otros (Cuñados)"])

                    with t1:
                        padres = [f for f in familia if f['TIPO'] in ['PADRE', 'MADRE']]
                        if padres:
                            for p in padres:
                                st.markdown(f"**{p['TIPO']}:** {p['NOMBRES']} {p['APELLIDOS']}  \n"
                                            f"🆔 DNI: `{p['DNI']}` | 🎂 Edad: {p['EDAD']} años")
                                st.divider()
                        else: st.info("No se registraron padres.")

                    with t2:
                        hermanos = [f for f in familia if 'HERMANO' in f['TIPO']]
                        if hermanos:
                            for h in hermanos:
                                st.markdown(f"👤 **{h['TIPO']}:** {h['NOMBRES']} {h['APELLIDOS']}  \n"
                                            f"🆔 DNI: `{h['DNI']}` | 🎂 Edad: {h['EDAD']} años")
                        else: st.info("No se registraron hermanos.")

                    with t3:
                        sobrinos = [f for f in familia if 'SOBRIN' in f['TIPO']]
                        if sobrinos:
                            for s in sobrinos:
                                st.success(f"👶 **{s['TIPO']}:** {s['NOMBRES']} {s['APELLIDOS']} (DNI: {s['DNI']})")
                        else: st.info("No se registraron sobrinos.")

                    with t4:
                        otros = [f for f in familia if f['TIPO'] not in ['PADRE', 'MADRE', 'HERMANO', 'HERMANA', 'SOBRINO', 'SOBRINA']]
                        if otros:
                            for o in otros:
                                st.warning(f"🤝 **{o['TIPO']}:** {o['NOMBRES']} {o['APELLIDOS']} (DNI: {o['DNI']})")
                        else: st.info("No hay otros vínculos registrados.")

                else:
                    st.error(f"Error: {data.get('message', 'No se encontraron resultados.')}")
            else:
                st.error(f"Error de servidor: {response.status_code}")
                
        except Exception as e:
            st.error(f"Ocurrió un error: {e}")

if __name__ == "__main__":
    run()
