import streamlit as st
import requests

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="DNI Básico PRO", layout="wide")

# --- ESTILOS ---
st.markdown("""
<style>
    .stApp { background-color: #0b0e14; }
    .main-card { background: #161b22; border: 1px solid #30363d; border-radius: 15px; padding: 25px; }
    .info-table { width: 100%; border-collapse: collapse; margin-top: 15px; border: 1px solid #30363d; border-radius: 8px; overflow: hidden; }
    .info-table td { padding: 14px; border-bottom: 1px solid #21262d; color: #c9d1d9; font-size: 0.85rem; }
    .info-table td:first-child { background: #0d1117; color: #8b949e; font-weight: bold; width: 40%; text-transform: uppercase; font-size: 0.7rem; }
    [data-testid="stImage"] { border: 4px solid #30363d; border-radius: 15px; padding: 5px; background: #161b22; }
</style>
""", unsafe_allow_html=True)

# --- LÓGICA DE EXTRACCIÓN MEJORADA ---
def find_data(obj, keys, default="N/D"):
    if not isinstance(obj, dict): return default
    for k in keys:
        if k in obj and obj[k]:
            val = str(obj[k]).strip()
            if val.lower() not in ["none", "null", ""]: return val.upper()
    return default

# --- UI LATERAL ---
c_left, c_right = st.columns([1.2, 3])

with c_left:
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.subheader("🆓 Consulta Básica")
    dni = st.text_input("INGRESE DNI", max_chars=8, placeholder="45106211")
    
    if st.button("EJECUTAR BÚSQUEDA", use_container_width=True, type="primary"):
        URL = "https://seeker-v6.com/personas/apiBasico/dni"
        HEADERS = {"Authorization": "Bearer sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"}
        PAYLOAD = {"dni": dni}
        
        try:
            r = requests.post(URL, headers=HEADERS, data=PAYLOAD)
            st.session_state.result_basico = r.json()
        except Exception as e:
            st.error(f"Error de conexión: {str(e)}")
            
    if st.button("🏠 VOLVER"): st.switch_page("app.py")
    st.markdown('</div>', unsafe_allow_html=True)

# --- RESULTADOS ---
if 'result_basico' in st.session_state:
    res = st.session_state.result_basico
    
    if res.get("status") == "success":
        data = res.get("data", {})
        col1, col2 = c_right.columns([2, 1])
        
        with col1:
            st.markdown('<h3 style="color:#10b981; margin:0;">✅ Datos Encontrados</h3>', unsafe_allow_html=True)
            
            campos = [
                ("Nombres", ["nombres", "nombre"]),
                ("Ap. Paterno", ["apellidoPaterno", "paterno", "ap_paterno"]),
                ("Ap. Materno", ["apellidoMaterno", "materno", "ap_materno"]),
                ("DNI / Doc", ["numeroDocumento", "dni", "documento"]),
                ("Cod. Verifica", ["digitoVerificacion", "codVerifica"]),
                ("Créditos", ["creditos_restantes"]) # Nota: Este suele estar en el root (res)
            ]
            
            tbl = '<table class="info-table">'
            for label, keys in campos:
                # Buscamos créditos en la raíz, lo demás en data
                target = res if label == "Créditos" else data
                val = find_data(target, keys)
                tbl += f'<tr><td>{label}</td><td style="font-weight:700;">{val}</td></tr>'
            tbl += '</table>'
            st.markdown(tbl, unsafe_allow_html=True)
            
        with col2:
            st.markdown('<p style="color:#8b949e; font-size:0.7rem; font-weight:bold; text-align:center;">FOTO RENIEC</p>', unsafe_allow_html=True)
            foto_keys = ["foto", "foto_base64", "fotografia"]
            foto_raw = find_data(data, foto_keys, None)
            if foto_raw:
                if not foto_raw.startswith("data:image"):
                    foto_raw = f"data:image/jpeg;base64,{foto_raw}"
                st.image(foto_raw, use_container_width=True)
            else:
                st.warning("Sin foto")
    else:
        # SI EL STATUS NO ES SUCCESS, MOSTRAMOS EL POR QUÉ
        msg = res.get("message", "Error desconocido en la API")
        c_right.error(f"⚠️ LA API RESPONDIÓ: {msg}")
        c_right.info("Verifica que tu DNI sea correcto y que tu token tenga créditos.")
