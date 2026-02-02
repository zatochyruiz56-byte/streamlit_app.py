import streamlit as st
import requests

# 1. CONFIGURACIÓN
st.set_page_config(page_title="DataAPI - Consulta Premium", layout="wide")

# 2. CSS AVANZADO (FIX DE FOTO Y TABLA)
st.markdown("""
<style>
    /* Fondo general */
    .stApp { background-color: #0b0e14; color: #c9d1d9; }
    
    /* Panel de búsqueda */
    .search-panel {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 20px;
        border-top: 4px solid #6366f1;
    }
    
    /* Tabla de resultados */
    .pro-table {
        width: 100%;
        border-collapse: collapse;
        background: #161b22;
        border-radius: 8px;
        border: 1px solid #30363d;
        overflow: hidden;
    }
    .pro-table td {
        padding: 14px 20px;
        border-bottom: 1px solid #21262d;
        font-size: 0.95rem;
    }
    .pro-table td:first-child {
        color: #8b949e;
        font-weight: 600;
        width: 40%;
        text-transform: uppercase;
        font-size: 0.75rem;
        letter-spacing: 0.5px;
    }
    
    /* ESTILO DIRECTO PARA LA FOTO (FIX) */
    [data-testid="stImage"] {
        border: 3px solid #30363d;
        border-radius: 16px;
        background: #161b22;
        padding: 10px;
        box-shadow: 0 15px 40px rgba(0,0,0,0.6);
        margin-top: 10px;
        transition: transform 0.3s ease;
    }
    [data-testid="stImage"]:hover {
        border-color: #6366f1;
        transform: scale(1.02);
    }
    
    /* Titulo de resultados */
    .result-header {
        color: #6366f1;
        font-size: 1.6rem;
        font-weight: 900;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
</style>
""", unsafe_allow_html=True)

# 3. FUNCIONES DE APOYO
def get_safe(data, keys, default="No disponible"):
    if not isinstance(data, dict): return default
    for k in keys:
        v = data.get(k)
        if v and str(v).strip() not in ["", "None", "null", "N/A"]:
            return str(v).upper()
    return default

def get_photo_url(data):
    # Intentar corregir el Base64 si viene sin cabecera
    keys = ['foto', 'foto_base64', 'foto_b64', 'fotografia', 'fotoBiometrica']
    for k in keys:
        raw = data.get(k)
        if raw and isinstance(raw, str) and len(raw) > 100:
            if not raw.startswith('data:image'):
                return f"data:image/jpeg;base64,{raw}"
            return raw
    return None

# 4. ESTRUCTURA DE COLUMNAS
c_search, c_main, c_photo = st.columns([1.1, 2.2, 1.2], gap="large")

if 'res' not in st.session_state:
    st.session_state.res = None

with c_search:
    st.markdown('<div class="search-panel">', unsafe_allow_html=True)
    st.title("👤 Consulta")
    st.caption("Premium Seeker V6")
    
    dni = st.text_input("DNI A CONSULTAR", max_chars=8, placeholder="60799566")
    
    if st.button("EJECUTAR BÚSQUEDA", use_container_width=True, type="primary"):
        with st.spinner("Cargando base de datos..."):
            try:
                TOKEN = "sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"
                url = "https://seeker-v6.com/personas/apiPremium/dni"
                r = requests.post(url, headers={"Authorization": f"Bearer {TOKEN}"}, data={"dni": dni})
                st.session_state.res = r.json()
            except:
                st.error("Fallo en la conexión")
    
    if st.button("🔙 SALIR", use_container_width=True):
        st.switch_page("app.py")
    st.markdown('</div>', unsafe_allow_html=True)

# 5. MOSTRAR DATOS
if st.session_state.res:
    res = st.session_state.res
    data = res.get("data", res) if isinstance(res, dict) else res
    
    with c_main:
        st.markdown('<div class="result-header">💎 Resultados Premium</div>', unsafe_allow_html=True)
        
        campos = [
            ("DNI / DOC", ["dni", "documento"]),
            ("NOMBRE COMPLETO", ["nombres", "nombre"]),
            ("AP. PATERNO", ["ap_paterno", "paterno"]),
            ("AP. MATERNO", ["ap_materno", "materno"]),
            ("NOMBRE PADRE", ["padre", "nombre_padre", "padre_nombre"]),
            ("NOMBRE MADRE", ["madre", "nombre_madre", "madre_nombre"]),
            ("FEC. NACIMIENTO", ["fec_nacimiento", "fecha_nacimiento"]),
            ("EDAD ACTUAL", ["edad"]),
            ("SEXO / GÉNERO", ["género", "sexo"]),
            ("ESTADO CIVIL", ["estado_civil"]),
            ("UBICACIÓN", ["dirección", "distrito"])
        ]
        
        table_body = ""
        for label, keys in campos:
            val = get_safe(data, keys)
            color = "#ffffff" if val != "No disponible" else "#484f58"
            table_body += f'<tr><td>{label}</td><td style="color:{color}; font-weight:700;">{val}</td></tr>'
            
        st.markdown(f'<table class="pro-table">{table_body}</table>', unsafe_allow_html=True)

    with c_photo:
        st.markdown('<div style="text-align:center; margin-bottom:10px; color:#8b949e; font-size:0.7rem; font-weight:bold; letter-spacing:1px;">IDENTIDAD BIOMÉTRICA</div>', unsafe_allow_html=True)
        photo = get_photo_url(data)
        if photo:
            st.image(photo, use_container_width=True)
        else:
            st.info("No se encontró fotografía para este documento.")
            st.markdown('<div style="height:300px; border:1px dashed #30363d; border-radius:15px; display:flex; align-items:center; justify-content:center; color:#484f58;">SIN FOTO</div>', unsafe_allow_html=True)
