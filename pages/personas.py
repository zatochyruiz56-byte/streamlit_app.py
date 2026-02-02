import streamlit as st
import requests

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="DataAPI - Multi Consulta", layout="wide")

# 2. ESTILOS CSS REFORZADOS
st.markdown("""
<style>
    .stApp { background-color: #0b0e14; color: #c9d1d9; }
    
    /* Panel de búsqueda */
    .search-panel {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 20px;
        border-left: 5px solid #3b82f6;
    }
    
    /* Estilo para la Tabla */
    .pro-table {
        width: 100%;
        border-collapse: collapse;
        background: #161b22;
        border-radius: 8px;
        border: 1px solid #30363d;
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
    
    /* ESTILO FIX PARA FOTO ENCAJADA */
    [data-testid="stImage"] {
        border: 3px solid #30363d;
        border-radius: 16px;
        background: #161b22;
        padding: 8px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        display: block;
        margin-left: auto;
        margin-right: auto;
    }

    .header-text {
        color: #3b82f6;
        font-size: 1.5rem;
        font-weight: 800;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# 3. FUNCIONES DE LIMPIEZA
def clean_val(data, keys, default="No disponible"):
    if not isinstance(data, dict): return default
    for k in keys:
        v = data.get(k)
        if v and str(v).strip() not in ["", "None", "null", "N/A"]:
            return str(v).upper()
    return default

def get_photo(data):
    keys = ['foto', 'foto_base64', 'foto_b64', 'fotografia', 'fotoBiometrica']
    for k in keys:
        raw = data.get(k)
        if raw and isinstance(raw, str) and len(raw) > 100:
            if not raw.startswith('data:image'):
                return f"data:image/jpeg;base64,{raw}"
            return raw
    return None

# 4. LAYOUT DE TRES COLUMNAS
c1, c2, c3 = st.columns([1, 2, 1], gap="large")

if 'api_res' not in st.session_state:
    st.session_state.api_res = None

with c1:
    st.markdown('<div class="search-panel">', unsafe_allow_html=True)
    st.subheader("👤 Panel de Búsqueda")
    
    # NUEVO SELECTOR DE MODO
    modo = st.selectbox("TIPO DE CONSULTA", ["PREMIUM", "GRATIS (BÁSICO)"])
    dni_input = st.text_input("NUMERO DOCUMENTO*", max_chars=8, placeholder="45106211")
    
    if st.button("BUSCAR AHORA", use_container_width=True, type="primary"):
        TOKEN = "sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"
        
        # LOGICA DE ENDPOINT SEGÚN SELECCIÓN
        if "PREMIUM" in modo:
            URL = "https://seeker-v6.com/personas/apiPremium/dni"
        else:
            URL = "https://seeker-v6.com/personas/apiBasico/dni"
            
        with st.spinner("Consultando..."):
            try:
                r = requests.post(URL, headers={"Authorization": f"Bearer {TOKEN}"}, data={"dni": dni_input})
                st.session_state.api_res = r.json()
            except:
                st.error("Error en la conexión con la API")
                
    if st.button("🔙 VOLVER AL MENÚ", use_container_width=True):
        st.switch_page("app.py")
    st.markdown('</div>', unsafe_allow_html=True)

# 5. RESULTADOS
if st.session_state.api_res:
    res = st.session_state.api_res
    # Ambas APIs suelen devolver los datos dentro de un campo 'data'
    data = res.get("data", res) if isinstance(res, dict) else res
    
    with c2:
        st.markdown('<div class="header-text">💎 Resultados Pro</div>', unsafe_allow_html=True)
        campos = [
            ("DNI", ["dni", "num_doc", "documento"]),
            ("NOMBRES", ["nombres"]),
            ("APELLIDO PATERNO", ["paterno", "ap_paterno"]),
            ("APELLIDO MATERNO", ["materno", "ap_materno"]),
            ("PADRE", ["padre", "nombre_padre"]),
            ("MADRE", ["madre", "nombre_madre"]),
            ("FECHA NACIMIENTO", ["fec_nacimiento", "fecha_nacimiento"]),
            ("EDAD ACTUAL", ["edad"]),
            ("ESTADO CIVIL", ["estado_civil"]),
            ("DIRECCIÓN", ["dirección", "distrito"])
        ]
        
        html_table = '<table class="pro-table">'
        for label, keys in campos:
            v = clean_val(data, keys)
            color = "white" if v != "No disponible" else "#484f58"
            html_table += f'<tr><td>{label}</td><td style="color:{color}; font-weight:bold;">{v}</td></tr>'
        html_table += '</table>'
        st.markdown(html_table, unsafe_allow_html=True)

    with c3:
        st.markdown('<div style="text-align:center; color:#8b949e; font-size:0.7rem; font-weight:bold; margin-bottom:10px;">IDENTIDAD BIOMÉTRICA</div>', unsafe_allow_html=True)
        foto_final = get_photo(data)
        if foto_final:
            st.image(foto_final, use_container_width=True)
        else:
            st.warning("Sin foto disponible")
