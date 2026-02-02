import streamlit as st
import requests
import base64

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="DataAPI - Consulta Premium", layout="wide")

# 2. ESTILOS CSS REFORZADOS
st.markdown("""
<style>
    .stApp { background-color: #0b0e14; color: #c9d1d9; }
    
    .search-panel {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 20px;
        border-left: 4px solid #3b82f6;
    }
    
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
    
    .val-empty { color: #484f58; font-style: italic; }

    /* Contenedor de Foto con Tamaño Mínimo para asegurar visibilidad */
    .photo-frame {
        border: 2px solid #30363d;
        border-radius: 12px;
        background: #161b22;
        padding: 10px;
        min-height: 380px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
</style>
""", unsafe_allow_html=True)

# 3. UTILIDADES DE DATOS
def clean_val(data, keys, default="No disponible"):
    if not isinstance(data, dict): return default
    for k in keys:
        v = data.get(k)
        if v and str(v).strip() not in ["", "None", "null", "N/A"]:
            return str(v).upper()
    return default

def fix_photo(data):
    # Lista exhaustiva de posibles llaves para la foto
    photo_keys = ['foto', 'foto_base64', 'foto_b64', 'fotografia', 'fotoBiometrica', 'imagen', 'img']
    raw_photo = None
    
    for k in photo_keys:
        if data.get(k):
            raw_photo = data.get(k)
            break
    
    if not raw_photo: return None
    
    # Si es base64 y no tiene el encabezado, se lo ponemos
    if isinstance(raw_photo, str) and len(raw_photo) > 100:
        if not raw_photo.startswith('data:image'):
            return f"data:image/jpeg;base64,{raw_photo}"
    
    return raw_photo

# 4. LAYOUT PRINCIPAL (Ajustado para balancear la tabla y la foto)
col_search, col_main, col_photo = st.columns([1, 2, 1], gap="medium")

if 'api_res' not in st.session_state:
    st.session_state.api_res = None

with col_search:
    st.markdown('<div class="search-panel">', unsafe_allow_html=True)
    st.subheader("👤 Consulta Premium")
    dni_in = st.text_input("DNI (8 DÍGITOS)*", max_chars=8, placeholder="45106211")
    
    if st.button("BUSCAR AHORA", use_container_width=True, type="primary"):
        TOKEN = "sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"
        URL = "https://seeker-v6.com/personas/apiPremium/dni"
        with st.spinner("Conectando..."):
            try:
                r = requests.post(URL, headers={"Authorization": f"Bearer {TOKEN}"}, data={"dni": dni_in})
                if r.status_code == 200:
                    st.session_state.api_res = r.json()
                else:
                    st.error("Error en servidor")
            except:
                st.error("Error de conexión")
    
    if st.button("🔙 VOLVER AL MENÚ", use_container_width=True):
        st.switch_page("app.py")
    st.markdown('</div>', unsafe_allow_html=True)

# 5. RENDERIZADO DE RESULTADOS
if st.session_state.api_res:
    res = st.session_state.api_res
    # Extraer el objeto de datos real (soporta 'data' o directo)
    data = res.get("data", res) if isinstance(res, dict) else res
    
    with col_main:
        st.markdown('<div style="color:#3b82f6; font-size:1.4rem; font-weight:bold; margin-bottom:15px;">💎 Resultados Pro</div>', unsafe_allow_html=True)
        
        campos = [
            ("DNI", ["dni", "num_doc"]),
            ("NOMBRES", ["nombres"]),
            ("APELLIDO PATERNO", ["ap_paterno", "paterno"]),
            ("APELLIDO MATERNO", ["ap_materno", "materno"]),
            ("PADRE", ["padre", "nombre_padre"]),
            ("MADRE", ["madre", "nombre_madre"]),
            ("FECHA NACIMIENTO", ["fec_nacimiento"]),
            ("EDAD", ["edad"]),
            ("GÉNERO", ["género", "sexo"]),
            ("ESTADO CIVIL", ["estado_civil"]),
            ("DIRECCIÓN", ["dirección"]),
            ("CADUCIDAD", ["f_caducidad"])
        ]
        
        table = '<table class="pro-table">'
        for label, keys in campos:
            val = clean_val(data, keys)
            color = "white" if val != "No disponible" else "#484f58"
            table += f'<tr><td>{label}</td><td style="color:{color}; font-weight:bold;">{val}</td></tr>'
        table += '</table>'
        st.markdown(table, unsafe_allow_html=True)

    with col_photo:
        st.markdown('<div class="photo-frame">', unsafe_allow_html=True)
        final_photo = fix_photo(data)
        
        if final_photo:
            st.image(final_photo, use_container_width=True)
            st.markdown('<div style="color:#8b949e; font-size:0.6rem; margin-top:5px;">FOTOGRAFÍA RENIEC</div>', unsafe_allow_html=True)
        else:
            st.error("⚠️ FOTO NO RECIBIDA")
            st.info("La API no envió imagen para este DNI.")
        st.markdown('</div>', unsafe_allow_html=True)
