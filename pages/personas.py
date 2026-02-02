import streamlit as st
import requests

# 1. SEGURIDAD Y CONFIGURACIÓN (Basado en tu original)
st.set_page_config(page_title="DataAPI - Consulta Premium", layout="wide")

if not st.session_state.get('auth', False):
    st.error("⚠️ Acceso denegado. Por favor inicie sesión.")
    st.stop()

# 2. CSS DE ALTO NIVEL (Estilo Seeker-V6)
st.markdown("""
<style>
    .stApp { background-color: #0b0e14; color: #c9d1d9; }
    
    /* Panel de Búsqueda */
    .search-container {
        background: #161b22;
        border: 1px solid #30363d;
        border-left: 4px solid #2ea043;
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }
    
    /* Encabezado de Resultados */
    .res-header {
        color: #a371f7;
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 25px;
        display: flex;
        align-items: center;
        gap: 12px;
    }

    /* Tabla Pro */
    .data-table {
        width: 100%;
        border-collapse: collapse;
        background: #161b22;
        border-radius: 10px;
        overflow: hidden;
    }
    .data-table td {
        padding: 14px 18px;
        border-bottom: 1px solid #30363d;
        font-size: 0.95rem;
    }
    .data-table td:first-child {
        color: #8b949e;
        font-weight: 600;
        width: 40%;
        text-transform: uppercase;
        font-size: 0.7rem;
        letter-spacing: 0.5px;
    }
    
    /* Marco de Foto */
    .photo-frame {
        border: 4px solid #30363d;
        border-radius: 16px;
        padding: 4px;
        background: #161b22;
        box-shadow: 0 15px 45px rgba(0,0,0,0.7);
        text-align: center;
    }
    
    /* Botón Personalizado */
    .stButton>button {
        background-color: #238636 !important;
        border-radius: 8px !important;
        border: none !important;
        font-weight: bold !important;
    }
</style>
""", unsafe_allow_html=True)

# 3. MAPEO DE LLAVES REALES DE TU API
# Usamos las llaves exactas que me pasaste en el log
MAPEO = [
    ("dni", "N° Documento"),
    ("nombres", "Nombres"),
    ("ap_paterno", "Apellido Paterno"),
    ("ap_materno", "Apellido Materno"),
    ("fec_nacimiento", "Fec. Nacimiento"),
    ("edad", "Edad Actual"),
    ("género", "Género"),
    ("estado_civil", "Estado Civil"),
    ("gradoInstruccion", "Grado Instrucción"),
    ("dirección", "Dirección Domicilio"),
    ("ubi_dirección", "Ubigeo"),
    ("origen", "Lugar de Origen"),
    ("padre", "Nombre del Padre"),
    ("madre", "Nombre de la Madre"),
    ("f_caducidad", "Vencimiento DNI")
]

# Inicializar sesión para que no se borren los datos
if 'api_res' not in st.session_state:
    st.session_state.api_res = None

# 4. DISEÑO DE COLUMNAS (3 Columnas Pro)
col_search, col_main, col_aside = st.columns([1.2, 2.2, 1.5], gap="large")

with col_search:
    st.markdown('<div class="search-container">', unsafe_allow_html=True)
    st.subheader("👤 Consulta DNI")
    st.caption("Acceso Premium - Base RENIEC")
    dni_input = st.text_input("NUMERO DOCUMENTO*", max_chars=8, placeholder="Ej: 60799566")
    
    if st.button("BUSCAR AHORA", use_container_width=True):
        if len(dni_input) == 8:
            TOKEN = "sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"
            URL = "https://seeker-v6.com/personas/apiPremium/dni"
            with st.spinner("Consultando DB..."):
                try:
                    r = requests.post(URL, headers={"Authorization": f"Bearer {TOKEN}"}, data={"dni": dni_input})
                    if r.status_code == 200:
                        st.session_state.api_res = r.json()
                    else:
                        st.error("Error en la conexión con el servidor.")
                except Exception as e:
                    st.error(f"Fallo técnico: {e}")
    
    if st.button("🔙 VOLVER AL MENÚ", use_container_width=True):
        st.switch_page("app.py")
    st.markdown('</div>', unsafe_allow_html=True)

# 5. MOSTRAR RESULTADOS (Solo si hay data)
if st.session_state.api_res:
    res = st.session_state.api_res
    
    # Extraer la data interna si existe, o usar la raíz si viene plano
    data = res.get("data", res) if isinstance(res, dict) else res
    
    with col_main:
        st.markdown('<div class="res-header">💎 Resultados Premium <span style="color:white; font-size:0.7rem; opacity:0.5">knowlers.xyz</span></div>', unsafe_allow_html=True)
        
        table_html = '<table class="data-table">'
        for key, label in MAPEO:
            # Buscamos el valor con la llave exacta
            val = data.get(key, "---")
            if val and str(val).strip():
                table_html += f'<tr><td>{label}</td><td>{val}</td></tr>'
        table_html += '</table>'
        st.markdown(table_html, unsafe_allow_html=True)

    with col_aside:
        st.markdown('<div class="photo-frame">', unsafe_allow_html=True)
        # La foto suele venir en 'foto'. La mostramos con prioridad
        foto_content = data.get("foto")
        if foto_content:
            st.image(foto_content, use_container_width=True, caption="FOTOGRAFÍA RENIEC")
        else:
            st.info("📷 Foto no disponible para este registro")
        st.markdown('</div>', unsafe_allow_html=True)
