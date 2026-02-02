import streamlit as st
import requests

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="DNI Básico - Seeker", layout="wide")

# --- DISEÑO UI ---
st.markdown("""
<style>
    .stApp { background-color: #0b0e14; }
    .main-card {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 15px;
        padding: 25px;
    }
    .info-table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 15px;
    }
    .info-table td {
        padding: 12px;
        border-bottom: 1px solid #21262d;
        color: #c9d1d9;
    }
    .info-table td:first-child {
        color: #8b949e;
        font-weight: bold;
        width: 40%;
        font-size: 0.75rem;
        text-transform: uppercase;
    }
    [data-testid="stImage"] {
        border: 5px solid #30363d;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
</style>
""", unsafe_allow_html=True)

# --- FUNCIONES DE SEGURIDAD (ANTI-ERROR) ---
def get_val(obj, keys, default="N/D"):
    if not obj or not isinstance(obj, dict): return default
    for k in keys:
        v = obj.get(k)
        if v and str(v).strip() not in ["", "None", "null"]:
            return str(v).upper()
    return default

def get_photo(obj):
    # Si obj es nulo, esta función ya no rompe el programa
    if not obj or not isinstance(obj, dict): return None
    keys = ['foto', 'foto_base64', 'fotografia']
    for k in keys:
        raw = obj.get(k)
        if raw and isinstance(raw, str) and len(raw) > 50:
            return f"data:image/jpeg;base64,{raw}" if not raw.startswith('data') else raw
    return None

# --- ESTRUCTURA ---
c_side, c_main, c_foto = st.columns([1, 2, 1], gap="large")

with c_side:
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.subheader("🆓 DNI Básico")
    dni_input = st.text_input("DNI (8 dígitos)", max_chars=8)
    
    if st.button("BUSCAR", use_container_width=True, type="primary"):
        # VARIABLES SEGÚN TU DOCUMENTACIÓN
        URL = "https://seeker-v6.com/personas/apiBasico/dni"
        HEADERS = {"Authorization": "Bearer sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"}
        DATA = {"dni": dni_input}
        
        with st.spinner("Conectando..."):
            try:
                response = requests.post(URL, headers=HEADERS, data=DATA)
                st.session_state.basico_res = response.json()
            except:
                st.error("Error de servidor")
    
    if st.button("⬅️ VOLVER"): st.switch_page("app.py")
    st.markdown('</div>', unsafe_allow_html=True)

# --- RESULTADOS ---
if 'basico_res' in st.session_state and st.session_state.basico_res:
    res = st.session_state.basico_res
    # Extraemos 'data' con seguridad
    info = res.get("data", {}) if isinstance(res, dict) else {}
    
    with c_main:
        st.markdown('<h3 style="color:#3b82f6;">📋 Ficha de Consulta</h3>', unsafe_allow_html=True)
        campos = [
            ("NOMBRES", ["nombres"]),
            ("APELLIDO PATERNO", ["paterno", "apellidoPaterno"]),
            ("APELLIDO MATERNO", ["materno", "apellidoMaterno"]),
            ("DNI", ["dni", "numeroDocumento"]),
            ("CÓDIGO VERIF.", ["digitoVerificacion", "codVerifica"]),
            ("CRÉDITOS REST.", ["creditos_restantes"]) # Variable del root
        ]
        
        html = '<table class="info-table">'
        for label, keys in campos:
            # Si el campo es créditos, lo buscamos en el root del json
            val = get_val(info if label != "CRÉDITOS REST." else res, keys)
            html += f'<tr><td>{label}</td><td><b>{val}</b></td></tr>'
        html += '</table>'
        st.markdown(html, unsafe_allow_html=True)

    with c_foto:
        st.markdown('<p style="text-align:center; font-size:0.7rem; color:#8b949e;">FOTOGRAFÍA RENIEC</p>', unsafe_allow_html=True)
        img = get_photo(info)
        if img:
            st.image(img, use_container_width=True)
        else:
            st.info("Sin foto en modo Básico")
