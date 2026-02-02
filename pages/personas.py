import streamlit as st
import requests

# 1. CONFIGURACIÓN
st.set_page_config(page_title="DataAPI - Multi Consulta", layout="wide")

# 2. CSS DE ALTA CALIDAD
st.markdown("""
<style>
    .stApp { background-color: #0b0e14; color: #c9d1d9; }
    
    /* Panel de Búsqueda */
    .search-container {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 24px;
        border-top: 4px solid #10b981;
    }
    
    /* Estilo para la Tabla */
    .data-table {
        width: 100%;
        border-collapse: collapse;
        background: #161b22;
        border-radius: 10px;
        border: 1px solid #30363d;
        overflow: hidden;
    }
    .data-table td {
        padding: 14px 20px;
        border-bottom: 1px solid #21262d;
        font-size: 0.9rem;
    }
    .data-table td:first-child {
        color: #8b949e;
        font-weight: 600;
        width: 35%;
        text-transform: uppercase;
        font-size: 0.7rem;
        background: #0d1117;
    }
    
    /* FIX DE FOTO: ENCAJE PERFECTO */
    [data-testid="stImage"] {
        border: 4px solid #30363d;
        border-radius: 20px;
        background: #161b22;
        padding: 8px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.6);
        transition: transform 0.3s ease;
    }
    [data-testid="stImage"]:hover { transform: scale(1.03); border-color: #10b981; }

    .header-title { color: #10b981; font-size: 1.7rem; font-weight: 900; margin-bottom: 15px; }
</style>
""", unsafe_allow_html=True)

# 3. FUNCIONES DE SEGURIDAD (FIX DEL ERROR ATTRIBUTEERROR)
def clean_val(data, keys, default="No disponible"):
    # Si data es None o no es un diccionario, abortar con seguridad
    if data is None or not isinstance(data, dict):
        return default
    for k in keys:
        v = data.get(k)
        if v and str(v).strip() not in ["", "None", "null", "N/A"]:
            return str(v).upper()
    return default

def get_photo(data):
    # SI DATA ES NONE, NO HACER NADA (ESTO ARREGLA TU ERROR)
    if data is None or not isinstance(data, dict):
        return None
        
    keys = ['foto', 'foto_base64', 'foto_b64', 'fotografia', 'fotoBiometrica']
    for k in keys:
        raw = data.get(k)
        if raw and isinstance(raw, str) and len(raw) > 100:
            if not raw.startswith('data:image'):
                return f"data:image/jpeg;base64,{raw}"
            return raw
    return None

# 4. COLUMNAS
col_menu, col_info, col_img = st.columns([1.1, 2.2, 1.2], gap="medium")

if 'last_api_res' not in st.session_state:
    st.session_state.last_api_res = None

with col_menu:
    st.markdown('<div class="search-container">', unsafe_allow_html=True)
    st.title("🔍 Buscar")
    
    modo = st.selectbox("SERVICIO", ["💎 PREMIUM", "🆓 BÁSICO (GRATIS)"])
    dni_val = st.text_input("DNI A CONSULTAR", max_chars=8, placeholder="60799566")
    
    if st.button("EJECUTAR CONSULTA", use_container_width=True, type="primary"):
        TOKEN = "sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"
        
        # Endpoint según selección
        if "PREMIUM" in modo:
            URL = "https://seeker-v6.com/personas/apiPremium/dni"
        else:
            URL = "https://seeker-v6.com/personas/apiBasico/dni"
            
        with st.spinner("Procesando..."):
            try:
                # Python requests envía 'data' como application/x-www-form-urlencoded por defecto
                r = requests.post(URL, headers={"Authorization": f"Bearer {TOKEN}"}, data={"dni": dni_val})
                st.session_state.last_api_res = r.json()
            except Exception as e:
                st.error(f"Fallo de conexión")
    
    if st.button("🏠 MENU PRINCIPAL", use_container_width=True):
        st.switch_page("app.py")
    st.markdown('</div>', unsafe_allow_html=True)

# 5. RENDERIZADO DE RESULTADOS
if st.session_state.last_api_res:
    res = st.session_state.last_api_res
    
    # Manejo ultra-seguro de la estructura del JSON
    if res and isinstance(res, dict):
        # Intentamos sacar 'data', si no existe, usamos el objeto raíz
        data_final = res.get("data")
        if data_final is None: 
            data_final = res
            
        with col_info:
            st.markdown('<div class="header-title">📋 Datos Obtenidos</div>', unsafe_allow_html=True)
            
            campos_config = [
                ("DNI / DOCUMENTO", ["dni", "num_doc", "documento"]),
                ("NOMBRES", ["nombres"]),
                ("APELLIDO PATERNO", ["paterno", "ap_paterno"]),
                ("APELLIDO MATERNO", ["materno", "ap_materno"]),
                ("PADRE", ["padre", "nombre_padre"]),
                ("MADRE", ["madre", "nombre_madre"]),
                ("NACIMIENTO", ["fec_nacimiento", "fecha_nacimiento"]),
                ("EDAD", ["edad"]),
                ("GÉNERO", ["género", "sexo"]),
                ("DIRECCIÓN", ["dirección", "distrito"])
            ]
            
            table_html = '<table class="data-table">'
            for label, keys in campos_config:
                val = clean_val(data_final, keys)
                text_color = "#ffffff" if val != "No disponible" else "#484f58"
                table_html += f'<tr><td>{label}</td><td style="color:{text_color}; font-weight:700;">{val}</td></tr>'
            table_html += '</table>'
            st.markdown(table_html, unsafe_allow_html=True)

        with col_img:
            st.markdown('<div style="text-align:center; color:#8b949e; font-size:0.65rem; font-weight:bold; margin-bottom:12px; letter-spacing:1px;">BIOMETRÍA RENIEC</div>', unsafe_allow_html=True)
            foto_base64 = get_photo(data_final)
            if foto_base64:
                st.image(foto_base64, use_container_width=True)
            else:
                st.info("Sin registro fotográfico")
    else:
        st.warning("La API no devolvió un formato válido.")
