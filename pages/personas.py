import streamlit as st
import requests

# --- CONFIGURACIÓN ---
st.set_page_config(layout="wide", page_title="Consulta Personas Pro")

# --- CSS PROFESIONAL ---
st.markdown("""
<style>
    .main { background-color: #0b0e14; }
    .stApp { background-color: #0b0e14; color: #c9d1d9; }
    
    .search-card {
        background: #161b22;
        border: 1px solid #30363d;
        border-left: 4px solid #2ea043;
        border-radius: 8px;
        padding: 20px;
    }
    
    .res-header {
        color: #a371f7;
        font-size: 1.3rem;
        font-weight: bold;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .info-table {
        width: 100%;
        border-collapse: collapse;
        background: #161b22;
        border-radius: 10px;
        overflow: hidden;
    }
    .info-table td {
        padding: 12px 15px;
        border-bottom: 1px solid #30363d;
        font-size: 0.9rem;
    }
    .info-table td:first-child {
        color: #8b949e;
        font-weight: 600;
        width: 35%;
        text-transform: uppercase;
        font-size: 0.75rem;
    }
    .info-table td:last-child {
        color: #f0f6fc;
    }
    
    .photo-container {
        border: 2px solid #30363d;
        border-radius: 12px;
        padding: 5px;
        background: #161b22;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
</style>
""", unsafe_allow_html=True)

# --- LÓGICA DE DICCIONARIO PARA ETIQUETAS ---
FIELD_LABELS = {
    "dni": "DNI / Documento",
    "nombres": "Nombres Completos",
    "ap_paterno": "Apellido Paterno",
    "ap_materno": "Apellido Materno",
    "edad": "Edad Actual",
    "género": "Género",
    "fec_nacimiento": "Fecha de Nacimiento",
    "padre": "Nombre del Padre",
    "madre": "Nombre de la Madre",
    "dirección": "Dirección Domicilio",
    "ubi_dirección": "Ubigeo (Residencia)",
    "origen": "Lugar de Nacimiento",
    "fec_emisión": "Fecha de Emisión DNI",
    "fec_inscripción": "Fecha de Inscripción",
    "f_caducidad": "Fecha de Caducidad",
    "gradoInstruccion": "Grado de Instrucción",
    "estado_civil": "Estado Civil",
    "estatura": "Estatura (m)",
    "deRestriccion": "Restricciones"
}

# --- LAYOUT PRINCIPAL ---
col_form, col_data, col_photo = st.columns([1.3, 2.2, 1.5], gap="large")

with col_form:
    st.markdown('<div class="search-card">', unsafe_allow_html=True)
    st.subheader("🔍 Buscador")
    dni_input = st.text_input("NUMERO DOC*", max_chars=8, placeholder="60799566")
    btn_buscar = st.button("BUSCAR AHORA", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

if btn_buscar and len(dni_input) == 8:
    TOKEN = "sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"
    URL = "https://seeker-v6.com/personas/apiPremium/dni"
    
    with st.spinner("Consultando Base de Datos..."):
        try:
            r = requests.post(URL, headers={"Authorization": f"Bearer {TOKEN}"}, data={"dni": dni_input})
            if r.status_code == 200:
                res = r.json()
                
                with col_data:
                    st.markdown('<div class="res-header">💎 Resultados Pro <span style="color:white; font-size:0.8rem; opacity:0.6">knowlers.xyz</span></div>', unsafe_allow_html=True)
                    
                    html_table = '<table class="info-table">'
                    for key, label in FIELD_LABELS.items():
                        val = res.get(key, "No disponible")
                        if val and str(val).strip():
                            html_table += f'<tr><td>{label}</td><td>{val}</td></tr>'
                    html_table += '</table>'
                    st.markdown(html_table, unsafe_allow_html=True)

                with col_photo:
                    st.markdown('<div class="photo-container">', unsafe_allow_html=True)
                    # La foto viene en el campo "foto", asumimos que es una URL o Base64
                    foto_url = res.get("foto")
                    if foto_url:
                        st.image(foto_url, use_container_width=True)
                    else:
                        st.warning("Foto no disponible")
                    st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.error("Error al conectar con la API")
        except Exception as e:
            st.error(f"Error crítico: {e}")
