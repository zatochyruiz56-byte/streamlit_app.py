import streamlit as st
import requests

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(layout="wide", page_title="Consulta RENIEC Pro", page_icon="👤")

# 2. CSS PARA EL ESTILO "SEEKER-V6"
st.markdown("""
<style>
    .stApp { background-color: #0b0e14; color: #c9d1d9; }
    [data-testid="stSidebar"] { display: none; } /* Ocultar sidebar si molesta */
    
    .search-card {
        background: #161b22;
        border: 1px solid #30363d;
        border-top: 3px solid #2ea043;
        border-radius: 12px;
        padding: 25px;
    }
    .res-header {
        color: #a371f7;
        font-size: 1.4rem;
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
    }
    .info-table td {
        padding: 12px 15px;
        border-bottom: 1px solid #30363d;
        font-size: 0.95rem;
    }
    .info-table td:first-child {
        color: #8b949e;
        font-weight: 600;
        width: 40%;
        text-transform: uppercase;
        font-size: 0.75rem;
    }
    .photo-container {
        border: 3px solid #30363d;
        border-radius: 15px;
        overflow: hidden;
        background: #161b22;
        box-shadow: 0 10px 40px rgba(0,0,0,0.6);
    }
</style>
""", unsafe_allow_html=True)

# 3. MAPEO EXACTO DE TU JSON (CON ACENTOS)
FIELD_LABELS = [
    ("dni", "DNI"),
    ("nombres", "Nombres"),
    ("ap_paterno", "Apellido Paterno"),
    ("ap_materno", "Apellido Materno"),
    ("edad", "Edad"),
    ("género", "Género"),
    ("fec_nacimiento", "Fecha de Nacimiento"),
    ("padre", "Padre"),
    ("madre", "Madre"),
    ("dirección", "Dirección"),
    ("ubi_dirección", "Ubigeo Dirección"),
    ("origen", "Lugar de Origen"),
    ("f_caducidad", "Fecha Caducidad"),
    ("gradoInstruccion", "Grado Instrucción")
]

# 4. INICIALIZAR ESTADO (Para que los datos no se borren al tocar la pantalla)
if 'results' not in st.session_state:
    st.session_state.results = None

# 5. LAYOUT DE COLUMNAS
col_form, col_data, col_photo = st.columns([1.2, 2, 1.5], gap="large")

with col_form:
    st.markdown('<div class="search-card">', unsafe_allow_html=True)
    st.markdown("### 🔍 Buscador")
    dni_input = st.text_input("NUMERO DOC*", max_chars=8, key="dni_input")
    
    if st.button("BUSCAR AHORA", use_container_width=True, type="primary"):
        if len(dni_input) == 8:
            TOKEN = "sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"
            URL = "https://seeker-v6.com/personas/apiPremium/dni"
            with st.spinner("Consultando..."):
                try:
                    r = requests.post(URL, headers={"Authorization": f"Bearer {TOKEN}"}, data={"dni": dni_input})
                    if r.status_code == 200:
                        st.session_state.results = r.json()
                    else:
                        st.error(f"Error {r.status_code}: No se pudo obtener respuesta.")
                except Exception as e:
                    st.error(f"Fallo de conexión: {e}")
    st.markdown('</div>', unsafe_allow_html=True)

# 6. RENDERIZADO CONDICIONAL (SOLO SI HAY RESULTADOS)
if st.session_state.results:
    res = st.session_state.results
    
    with col_data:
        st.markdown('<div class="res-header">✨ Resultados Pro <span style="color:white; font-size:0.8rem">knowlers.xyz</span></div>', unsafe_allow_html=True)
        
        table_html = '<table class="info-table">'
        for key, label in FIELD_LABELS:
            val = res.get(key, "-")
            table_html += f'<tr><td>{label}</td><td>{val}</td></tr>'
        table_html += '</table>'
        st.markdown(table_html, unsafe_allow_html=True)
        
    with col_photo:
        st.markdown('<div class="photo-container">', unsafe_allow_html=True)
        foto_url = res.get("foto")
        if foto_url:
            st.image(foto_url, use_container_width=True)
        else:
            st.warning("⚠️ Foto no disponible en la API")
        st.markdown('</div>', unsafe_allow_html=True)
