import streamlit as st
import requests

def run():
    # Estilos CSS para calcar la web del MTC
    st.markdown("""
        <style>
        .mtc-container { font-family: 'Arial', sans-serif; color: #333; }
        .mtc-title { font-size: 24px; text-align: center; margin-bottom: 30px; color: #333; }
        .section-header { font-size: 18px; font-weight: bold; margin-bottom: 15px; border-bottom: none; }
        .label { color: #888; font-size: 12px; margin-bottom: 0px; }
        .value { font-size: 15px; border-bottom: 1px solid #ccc; padding-bottom: 2px; margin-bottom: 15px; min-height: 22px; text-transform: uppercase; }
        .tab-container { display: flex; border-bottom: 1px solid #ddd; margin-bottom: 20px; }
        .tab { padding: 10px 20px; color: #777; font-weight: bold; display: flex; align-items: center; gap: 5px; cursor: default; }
        .tab.active { color: #d32f2f; border-bottom: 3px solid #d32f2f; }
        .vigente { color: #2e7d32; font-weight: bold; }
        .plus-button { 
            position: fixed; bottom: 30px; right: 30px; background-color: #b71c1c; 
            color: white; border-radius: 50%; width: 50px; height: 50px; 
            display: flex; align-items: center; justify-content: center; font-size: 30px; 
            box-shadow: 0 4px 8px rgba(0,0,0,0.3); z-index: 1000;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='mtc-title'>Consulta de Licencia de Conducir</div>", unsafe_allow_html=True)

    # Lógica de API (Factiliza)
    TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI0MDMwNSIsImh0dHA6Ly9zY2hlbWFzLm1pY3Jvc29mdC5jb20vd3MvMjAwOC8wNi9pZGVudGl0eS9jbGFpbXMvcm9sZSI6ImNvbnN1bHRvciJ9.Gsokm2AIDVCMdG5etymgkljwqXoCrb7b24c75H_VMr0"
    headers = {"Authorization": f"Bearer {TOKEN}"}
    
    dni = st.text_input("Ingrese DNI para buscar:")

    if dni:
        url = f"https://api.factiliza.com/v1/licencia/info/{dni}"
        res = requests.get(url, headers=headers).json()
        
        if res.get("status") == 200:
            d = res["data"]
            l = d["licencia"]
            
            # Procesar nombre para separar apellidos de nombres
            partes = d.get('nombre_completo', '').split()
            apellidos = " ".join(partes[-2:]) if len(partes) >= 2 else ""
            nombres = " ".join(partes[:-2]) if len(partes) >= 2 else d.get('nombre_completo')

            # --- BLOQUE 1: DATOS DEL CONDUCTOR ---
            st.markdown("<div class='section-header'>Datos del conductor</div>", unsafe_allow_html=True)
            c1, c2, c3 = st.columns([2, 2, 1])
            with c1:
                st.markdown(f"<p class='label'>Apellidos</p><div class='value'>{apellidos}</div>", unsafe_allow_html=True)
                st.markdown(f"<p class='label'>Tipo de documento</p><div class='value'>DNI</div>", unsafe_allow_html=True)
            with c2:
                st.markdown(f"<p class='label'>Nombres</p><div class='value'>{nombres}</div>", unsafe_allow_html=True)
                st.markdown(f"<p class='label'>Número de documento</p><div class='value'>{d.get('numero_documento')}</div>", unsafe_allow_html=True)
            with c3:
                st.image("https://i.imgur.com/8v98V9m.png", width=100) # Imagen del carnet azul

            # --- BLOQUE 2: PESTAÑAS (TABS) ---
            st.markdown("""
                <div class='tab-container'>
                    <div class='tab active'>🎴 Licencias</div>
                    <div class='tab'>🔴 Puntos</div>
                    <div class='tab'>📂 Record</div>
                    <div class='tab'>📝 Papeletas Impagas</div>
                    <div class='tab'>🗂️ Trámites</div>
                </div>
            """, unsafe_allow_html=True)

            # --- BLOQUE 3: DETALLE DE LICENCIA ---
            st.markdown(f"**Licencia: {l.get('categoria')} - <span class='vigente'>{l.get('estado')}</span>**", unsafe_allow_html=True)
            
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown(f"<p class='label'>Clase y categoría</p><div class='value'>{l.get('categoria')}</div>", unsafe_allow_html=True)
                st.markdown(f"<p class='label'>Tipo de Licencia</p><div class='value'>ELECTRÓNICA 📄</div>", unsafe_allow_html=True)
                st.markdown(f"<p class='label'>Restricciones</p><div class='value'>{l.get('restricciones')}</div>", unsafe_allow_html=True)
            with col_b:
                st.markdown(f"<p class='label'>Número de licencia</p><div class='value'>{l.get('numero')}</div>", unsafe_allow_html=True)
                st.markdown(f"<p class='label'>Fecha de expedición</p><div class='value'>{l.get('fecha_expedicion') if l.get('fecha_expedicion') else '---'}</div>", unsafe_allow_html=True)
                st.markdown(f"<p class='label'>Vigente hasta</p><div class='value'>{l.get('fecha_vencimiento')}</div>", unsafe_allow_html=True)

            # Botón flotante rojo del MTC
            st.markdown("<div class='plus-button'>+</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    run()
