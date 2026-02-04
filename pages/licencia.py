import streamlit as st
import requests

def run():
    # Configuración de estilo para imitar el portal del MTC
    st.markdown("""
        <style>
        .mtc-header { color: #333; font-family: sans-serif; font-weight: bold; margin-bottom: 20px; }
        .label-gray { color: #666; font-size: 0.8rem; margin-bottom: 2px; }
        .data-value { color: #333; font-size: 1rem; border-bottom: 1px solid #ccc; padding-bottom: 5px; margin-bottom: 15px; text-transform: uppercase; }
        .status-vigente { color: #28a745; font-weight: bold; }
        .tab-box { border-bottom: 2px solid #d9534f; color: #d9534f; font-weight: bold; padding: 10px; display: flex; align-items: center; gap: 8px; }
        </style>
    """, unsafe_allow_html=True)

    st.title("Consulta de Licencia de Conducir")

    TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI0MDMwNSIsImh0dHA6Ly9zY2hlbWFzLm1pY3Jvc29mdC5jb20vd3MvMjAwOC8wNi9pZGVudGl0eS9jbGFpbXMvcm9sZSI6ImNvbnN1bHRvciJ9.Gsokm2AIDVCMdG5etymgkljwqXoCrb7b24c75H_VMr0"
    headers = {"Authorization": f"Bearer {TOKEN}"}
    dni = st.text_input("Ingrese DNI:", max_chars=8)

    if st.button("Consultar"):
        url = f"https://api.factiliza.com/v1/licencia/info/{dni}"
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            res = response.json()
            if res.get("status") == 200:
                data = res["data"]
                lic = data["licencia"] # Extraemos objeto licencia

                # --- SECCIÓN: DATOS DEL CONDUCTOR ---
                st.markdown("<h4 class='mtc-header'>Datos del conductor</h4>", unsafe_allow_html=True)
                
                col1, col2, col_img = st.columns([2, 2, 1])
                with col1:
                    st.markdown(f"<p class='label-gray'>Apellidos</p><p class='data-value'>{data.get('nombre_completo', '').split()[-2:]}</p>", unsafe_allow_html=True)
                    st.markdown(f"<p class='label-gray'>Tipo de documento</p><p class='data-value'>DNI</p>", unsafe_allow_html=True)
                with col2:
                    st.markdown(f"<p class='label-gray'>Nombres</p><p class='data-value'>{data.get('nombre_completo', '').split()[:-2]}</p>", unsafe_allow_html=True)
                    st.markdown(f"<p class='label-gray'>Número de documento</p><p class='data-value'>{data.get('numero_documento')}</p>", unsafe_allow_html=True)
                with col_img:
                    st.image("https://cdn-icons-png.flaticon.com/512/1055/1055644.png", width=80) # Icono carnet azul

                # --- SECCIÓN: TABS (Iconos y Rojo MTC) ---
                st.markdown("""
                    <div style='display: flex; gap: 20px; border-bottom: 1px solid #ddd; margin-top: 20px;'>
                        <div class='tab-box'>🪪 Licencias</div>
                        <div style='color: #666; padding: 10px;'>🔴 Puntos</div>
                        <div style='color: #666; padding: 10px;'>📋 Record</div>
                        <div style='color: #666; padding: 10px;'>🧾 Papeletas</div>
                    </div>
                """, unsafe_allow_html=True)

                # --- SECCIÓN: DETALLE LICENCIA ---
                st.markdown(f"<br><p style='font-size: 1.1rem; font-weight: bold;'>Licencia: {lic.get('categoria')} - <span class='status-vigente'>{lic.get('estado')}</span></p>", unsafe_allow_html=True)
                
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown(f"<p class='label-gray'>Clase y categoría</p><p class='data-value'>{lic.get('categoria')}</p>", unsafe_allow_html=True)
                    st.markdown(f"<p class='label-gray'>Tipo de Licencia</p><p class='data-value'>ELECTRÓNICA 📄</p>", unsafe_allow_html=True)
                    st.markdown(f"<p class='label-gray'>Restricciones</p><p class='data-value'>{lic.get('restricciones')}</p>", unsafe_allow_html=True)
                with c2:
                    st.markdown(f"<p class='label-gray'>Número de licencia</p><p class='data-value'>{lic.get('numero')}</p>", unsafe_allow_html=True)
                    st.markdown(f"<p class='label-gray'>Fecha de expedición</p><p class='data-value'>{lic.get('fecha_expedicion', '---')}</p>", unsafe_allow_html=True)
                    st.markdown(f"<p class='label-gray'>Vigente hasta</p><p class='data-value'>{lic.get('fecha_vencimiento')}</p>", unsafe_allow_html=True)
            else:
                st.error("No se encontró información para el DNI ingresado.")
        else:
            st.error(f"Error en API: {response.status_code}")

if __name__ == "__main__":
    run()
