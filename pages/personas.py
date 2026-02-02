import streamlit as st
import requests

# 1. CONFIGURACIÓN Y SEGURIDAD
st.set_page_config(page_title="DataAPI - Consulta Premium", layout="wide")

if not st.session_state.get('auth', False):
    st.error("⚠️ Acceso denegado. Inicie sesión.")
    st.stop()

# 2. ESTILOS CSS PROFESIONALES
st.markdown("""
<style>
    .stApp { background-color: #0b0e14; color: #c9d1d9; }
    
    .search-panel {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 20px;
        border-left: 4px solid #a371f7;
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
    
    .family-box {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 10px;
        padding: 15px;
        margin-top: 10px;
    }
    .family-label { color: #8b949e; font-size: 0.7rem; font-weight: bold; text-transform: uppercase; }
    .family-value { color: #ffffff; font-size: 1rem; font-weight: bold; }

    .photo-container {
        border: 4px solid #30363d;
        border-radius: 12px;
        background: #161b22;
        padding: 5px;
        box-shadow: 0 20px 50px rgba(0,0,0,0.8);
    }
</style>
""", unsafe_allow_html=True)

# 3. FUNCIÓN PARA BUSCAR DATOS (Inteligente con llaves)
def get_val(data, keys, default="No disponible"):
    if not isinstance(data, dict): return default
    for k in keys:
        v = data.get(k)
        if v and str(v).strip() not in ["", "None", "null", "N/A"]:
            return str(v).upper()
    return default

# 4. MAPEO DE CAMPOS (Múltiples llaves por campo para seguridad)
# ("Etiqueta", ["llave1", "llave2", "llave3"])
CONFIG_CAMPOS = [
    ("DNI / DOCUMENTO", ["dni", "documento", "num_doc"]),
    ("NOMBRES", ["nombres", "nombre"]),
    ("APELLIDO PATERNO", ["ap_paterno", "apellido_paterno", "paterno"]),
    ("APELLIDO MATERNO", ["ap_materno", "apellido_materno", "materno"]),
    ("PADRE", ["padre", "nombre_padre", "padre_nombre"]),
    ("MADRE", ["madre", "nombre_madre", "madre_nombre"]),
    ("FEC. NACIMIENTO", ["fec_nacimiento", "fecha_nacimiento", "nacimiento"]),
    ("EDAD ACTUAL", ["edad"]),
    ("GÉNERO / SEXO", ["género", "sexo", "genero"]),
    ("ESTADO CIVIL", ["estado_civil"]),
    ("DIRECCIÓN", ["dirección", "direccion"]),
    ("UBIGEO", ["ubi_dirección", "ubigeo", "distrito"]),
    ("ESTATURA", ["estatura"]),
    ("RESTRICCIONES", ["deRestriccion", "restriccion", "observaciones"]),
    ("FEC. EMISIÓN", ["fec_emisión", "fecha_emision"]),
    ("FEC. CADUCIDAD", ["f_caducidad", "fecha_caducidad"])
]

if 'data_res' not in st.session_state:
    st.session_state.data_res = None

# 5. LAYOUT DE 3 COLUMNAS
col_search, col_main, col_photo = st.columns([1.2, 2.2, 1.5], gap="large")

with col_search:
    st.markdown('<div class="search-panel">', unsafe_allow_html=True)
    st.subheader("👤 Consulta Premium")
    st.caption("Base de Datos RENIEC Actualizada")
    
    dni_input = st.text_input("NUMERO DOCUMENTO*", max_chars=8, placeholder="60799566")
    
    if st.button("BUSCAR AHORA", use_container_width=True, type="primary"):
        if len(dni_input) == 8:
            TOKEN = "sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"
            URL = "https://seeker-v6.com/personas/apiPremium/dni"
            with st.spinner("Buscando en servidor..."):
                try:
                    r = requests.post(URL, headers={"Authorization": f"Bearer {TOKEN}"}, data={"dni": dni_input})
                    if r.status_code == 200:
                        st.session_state.data_res = r.json()
                    else:
                        st.error("Error en la conexión API.")
                except Exception as e:
                    st.error(f"Fallo técnico: {e}")
    
    if st.button("🔙 VOLVER AL MENÚ", use_container_width=True):
        st.switch_page("app.py")
    st.markdown('</div>', unsafe_allow_html=True)

# 6. MOSTRAR INFORMACIÓN
if st.session_state.data_res:
    res = st.session_state.data_res
    data = res.get("data", res) if isinstance(res, dict) else res
    
    with col_main:
        st.markdown('<div style="color:#a371f7; font-size:1.5rem; font-weight:bold; margin-bottom:15px;">💎 Resultados Pro</div>', unsafe_allow_html=True)
        
        # Tabla Principal
        table_html = '<table class="pro-table">'
        for label, keys in CONFIG_CAMPOS:
            val = get_val(data, keys)
            display_val = f'<b>{val}</b>' if val != "No disponible" else f'<span class="val-empty">{val}</span>'
            table_html += f'<tr><td>{label}</td><td>{display_val}</td></tr>'
        table_html += '</table>'
        st.markdown(table_html, unsafe_allow_html=True)
        
        # Sección Especial para Padres (Doble verificación)
        st.markdown('<div style="margin-top:25px; border-top:1px solid #30363d; padding-top:15px;">', unsafe_allow_html=True)
        st.subheader("👪 Datos Familiares Detallados")
        f1, f2 = st.columns(2)
        
        val_padre = get_val(data, ["padre", "nombre_padre", "padre_nombre"])
        val_madre = get_val(data, ["madre", "nombre_madre", "madre_nombre"])
        
        f1.markdown(f"""<div class="family-box"><div class="family-label">PADRE</div><div class="family-value">{val_padre}</div></div>""", unsafe_allow_html=True)
        f2.markdown(f"""<div class="family-box"><div class="family-label">MADRE</div><div class="family-value">{val_madre}</div></div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_photo:
        st.markdown('<div class="photo-container">', unsafe_allow_html=True)
        # Búsqueda de foto en múltiples campos
        foto_data = data.get("foto") or data.get("foto_base64")
        if foto_data:
            st.image(foto_data, use_container_width=True, caption="RENIEC BIOMETRÍA")
        else:
            st.warning("📷 Fotografía no disponible")
        st.markdown('</div>', unsafe_allow_html=True)
