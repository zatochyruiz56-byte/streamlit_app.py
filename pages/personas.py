import streamlit as st
import requests

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Consulta Premium - DataAPI", layout="wide")

# Validar Sesión (Tu lógica original)
if not st.session_state.get('auth', False):
    st.error("⚠️ Acceso denegado. Inicie sesión en la página principal.")
    st.stop()

# 2. ESTILO CSS SEEKER-V6 (Réplica Exacta)
st.markdown("""
<style>
    .stApp { background-color: #0b0e14; color: #c9d1d9; }
    
    /* Contenedor de Búsqueda Izquierdo */
    .search-panel {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 20px;
        border-image: linear-gradient(to bottom, #7928ca, #ff0080) 1; /* Borde gradiente opcional */
        border-left: 4px solid #a371f7;
    }
    
    .tab-active {
        background: #1f6feb;
        color: white;
        padding: 5px 15px;
        border-radius: 5px;
        font-weight: bold;
    }

    /* Tabla Central */
    .results-title {
        color: #a371f7;
        font-size: 1.4rem;
        font-weight: bold;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .pro-table {
        width: 100%;
        border-collapse: collapse;
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 8px;
    }
    .pro-table td {
        padding: 12px 20px;
        border-bottom: 1px solid #21262d;
        font-size: 0.9rem;
    }
    .pro-table td:first-child {
        color: #8b949e;
        font-weight: 600;
        width: 35%;
        text-transform: uppercase;
        font-size: 0.7rem;
    }
    .val-empty { color: #484f58; font-style: italic; }

    /* Marco de Foto Derecho */
    .photo-container {
        border: 4px solid #30363d;
        border-radius: 10px;
        padding: 5px;
        background: #161b22;
        box-shadow: 0 20px 50px rgba(0,0,0,0.8);
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# 3. LISTADO COMPLETO DE TODOS LOS CAMPOS POSIBLES
# Basado en el JSON premium de RENIEC
FIELD_MAP = [
    ("dni", "DNI / DOCUMENTO"),
    ("nombres", "NOMBRES COMPLETOS"),
    ("ap_paterno", "APELLIDO PATERNO"),
    ("ap_materno", "APELLIDO MATERNO"),
    ("padre", "NOMBRE DEL PADRE"),
    ("madre", "NOMBRE DE LA MADRE"),
    ("fec_nacimiento", "FECHA DE NACIMIENTO"),
    ("edad", "EDAD ACTUAL"),
    ("género", "GÉNERO / SEXO"),
    ("estado_civil", "ESTADO CIVIL"),
    ("estatura", "ESTATURA (CM)"),
    ("gradoInstruccion", "GRADO INSTRUCCIÓN"),
    ("dirección", "DIRECCIÓN ACTUAL"),
    ("ubi_dirección", "UBIGEO / DISTRITO"),
    ("origen", "LUGAR DE ORIGEN"),
    ("fec_emisión", "FECHA EMISIÓN DNI"),
    ("fec_inscripción", "FECHA INSCRIPCIÓN"),
    ("f_caducidad", "FECHA CADUCIDAD"),
    ("deRestriccion", "RESTRICCIONES")
]

# Estado persistente
if 'last_query' not in st.session_state:
    st.session_state.last_query = None

# 4. LAYOUT DE 3 COLUMNAS
c_search, c_main, c_photo = st.columns([1.2, 2.2, 1.5], gap="large")

with c_search:
    st.markdown('<div class="search-panel">', unsafe_allow_html=True)
    st.subheader("👤 Consulta Premium")
    
    # Tabs visuales (Simulados)
    st.markdown("""
        <div style="display:flex; gap:5px; margin-bottom:20px; font-size:10px;">
            <span class="tab-active">DNI</span>
            <span style="opacity:0.5">NOMBRE</span>
            <span style="opacity:0.5">PADRES</span>
            <span style="opacity:0.5">FULL</span>
        </div>
    """, unsafe_allow_html=True)
    
    dni_input = st.text_input("NUMERO DOC*", max_chars=8, placeholder="60799566")
    
    if st.button("BUSCAR AHORA", use_container_width=True, type="primary"):
        if len(dni_input) == 8:
            TOKEN = "sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"
            URL = "https://seeker-v6.com/personas/apiPremium/dni"
            with st.spinner("Conectando con RENIEC..."):
                try:
                    r = requests.post(URL, headers={"Authorization": f"Bearer {TOKEN}"}, data={"dni": dni_input})
                    if r.status_code == 200:
                        st.session_state.last_query = r.json()
                    else:
                        st.error("Error: Servicio no disponible temporalmente.")
                except Exception as e:
                    st.error(f"Error técnico: {e}")
        else:
            st.warning("El DNI debe tener 8 dígitos")

    if st.button("🔙 VOLVER", use_container_width=True):
        st.switch_page("app.py")
    st.markdown('</div>', unsafe_allow_html=True)

# 5. MOSTRAR RESULTADOS COMPLETOS
if st.session_state.last_query:
    res = st.session_state.last_query
    # Manejar si los datos vienen dentro de un objeto 'data' o en la raíz
    data = res.get("data", res) if isinstance(res, dict) else res
    
    with c_main:
        st.markdown('<div class="results-title">💎 Resultados Pro <span style="color:white; font-size:0.7rem; opacity:0.4">knowlers.xyz</span></div>', unsafe_allow_html=True)
        
        table_html = '<table class="pro-table">'
        for key, label in FIELD_MAP:
            val = data.get(key)
            # Lógica de "No disponible"
            if val is None or str(val).strip() == "" or str(val).lower() == "none":
                display_val = '<span class="val-empty">No disponible</span>'
            else:
                display_val = f'<b>{val}</b>'
            
            table_html += f'<tr><td>{label}</td><td>{display_val}</td></tr>'
        table_html += '</table>'
        st.markdown(table_html, unsafe_allow_html=True)

    with c_photo:
        st.markdown('<div class="photo-container">', unsafe_allow_html=True)
        # Buscar campo de foto (foto o foto_base64)
        foto = data.get("foto") or data.get("foto_base64")
        if foto:
            st.image(foto, use_container_width=True)
        else:
            st.warning("📷 Fotografía no disponible")
        st.markdown('</div>', unsafe_allow_html=True)
