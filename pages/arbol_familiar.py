import streamlit as st
import requests
import json

def run():
    st.set_page_config(layout="wide", page_title="Genealogía Pro")
    
    # Estilos CSS para tarjetas modernas sin imágenes
    st.markdown("""
        <style>
        .family-card {
            background-color: #f8fafc;
            border-left: 5px solid #64748b;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 10px;
            box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
        }
        .fallecido {
            border-left: 5px solid #ef4444 !important;
            background-color: #fef2f2;
        }
        .titular-box {
            background-color: #1e293b;
            color: white;
            padding: 20px;
            border-radius: 12px;
            margin-bottom: 25px;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1 style='text-align: center;'>🧬 Estructura Genealógica</h1>", unsafe_allow_html=True)

    TOKEN = "sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"
    dni_input = st.text_input("DNI del Titular", max_chars=8, placeholder="Ejm: 45106211")

    if st.button("🔍 ANALIZAR VÍNCULOS", use_container_width=True):
        try:
            url = "https://seeker-v6.com/personas/arbol-familiar"
            res = requests.get(url, headers={"Authorization": f"Bearer {TOKEN}"}, params={"dni": dni_input})
            
            if res.status_code == 200:
                data = res.json()
                if data.get("status") == "success":
                    info = data.get("infopersona", {})
                    arbol = data.get("arbol", [])

                    # --- SECCIÓN TITULAR ---
                    st.markdown(f"""
                        <div class="titular-box">
                            <h2 style='color: white; margin:0;'>{info.get('nombre_completo')}</h2>
                            <p style='margin:0;'>🆔 DNI: {info.get('dni')}  |  🎂 {info.get('edad')} años  |  📍 {info.get('ubicacion_completa')}</p>
                            <p style='margin:0; font-size: 0.9em; opacity: 0.8;'>Estado Civil: {info.get('estado_civil')} | Dirección: {info.get('direccion')}</p>
                        </div>
                    """, unsafe_allow_html=True)

                    # --- SECCIÓN ÁRBOL ---
                    st.subheader("👥 Red de Parentesco")
                    
                    # Definimos grupos y sus iconos
                    grupos = {
                        "PADRE/MADRE": ["PADRE", "MADRE"],
                        "HERMANOS": ["HERMANO", "HERMANA"],
                        "SOBRINOS": ["SOBRINO", "SOBRINA"],
                        "OTROS": ["CUÑADO", "CUÑADA", "TIO", "TIA"]
                    }

                    for titulo, tipos in grupos.items():
                        miembros = [m for m in arbol if m['TIPO'] in tipos]
                        if miembros:
                            st.markdown(f"#### {titulo}")
                            cols = st.columns(3)
                            for i, m in enumerate(miembros):
                                with cols[i % 3]:
                                    # Lógica de Fallecido (Edad > 90 o según API)
                                    es_fallecido = int(m['EDAD']) > 90
                                    clase = "family-card fallecido" if es_fallecido else "family-card"
                                    status_txt = "✟ POSIBLE FALLECIDO" if es_fallecido else "✓ ACTIVO"
                                    
                                    st.markdown(f"""
                                        <div class="{clase}">
                                            <small style='color: #64748b; font-weight: bold;'>{m['TIPO']}</small><br>
                                            <span style='font-size: 1.1em; font-weight: bold;'>{m['NOMBRES']} {m['APELLIDOS']}</span><br>
                                            <span style='font-size: 0.9em;'>🆔 DNI: {m['DNI']}</span><br>
                                            <span style='font-size: 0.9em;'>🎂 Edad: {m['EDAD']} años</span><br>
                                            <small style='color: {"#ef4444" if es_fallecido else "#10b981"};'>{status_txt}</small>
                                        </div>
                                    """, unsafe_allow_html=True)
                else:
                    st.error("DNI no encontrado.")
            else:
                st.error("Error en la conexión con la API.")
        except Exception as e:
            st.error(f"Error: {e}")

if __name__ == "__main__":
    run()
