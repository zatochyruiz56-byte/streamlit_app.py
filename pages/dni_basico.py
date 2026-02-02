import streamlit as st
import requests

# 1. Configuración
st.set_page_config(page_title="Buscador DNI", layout="wide")

# 2. CSS Estricto para evitar errores de renderizado
st.markdown("""
<style>
    .stApp { background-color: #0e1117; }
    
    /* Contenedor de la tabla */
    .data-card {
        background-color: #161b22;
        border-radius: 8px;
        border: 1px solid #30363d;
        overflow: hidden;
        margin-top: 10px;
    }

    /* Filas (Cajones) */
    .data-row {
        display: flex;
        border-bottom: 1px solid #30363d;
        padding: 15px 20px;
        align-items: center;
        background-color: #161b22;
    }
    .data-row:last-child { border-bottom: none; }

    /* Etiquetas Grises */
    .data-label {
        width: 45%;
        color: #8b949e;
        font-size: 11px;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* Valores Blancos */
    .data-value {
        width: 55%;
        color: #ffffff;
        font-weight: 700;
        font-size: 14px;
    }

    /* Título Verde */
    .premium-title {
        color: #00a36c;
        font-size: 22px;
        font-weight: bold;
        margin-bottom: 15px;
    }

    /* Marco de Foto */
    .photo-frame {
        border: 2px solid #30363d;
        border-radius: 12px;
        padding: 40px 20px;
        background: #161b22;
        text-align: center;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    .no-photo-text { color: #8b949e; font-size: 13px; font-weight: bold; }

    /* Ocultar basurilla de Streamlit */
    #MainMenu, footer, header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

def val(d, keys):
    if not isinstance(d, dict): return "NO DISPONIBLE"
    for k in keys:
        v = d.get(k)
        if v and str(v).strip().lower() not in ["none", "null", ""]:
            return str(v).upper()
    return "NO DISPONIBLE"

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='text-align:center;'>🔍 BUSCADOR</h2>", unsafe_allow_html=True)
    dni_input = st.text_input("DNI A CONSULTAR", max_chars=8)
    if st.button("EJECUTAR CONSULTA", type="primary", use_container_width=True):
        if len(dni_input) == 8:
            URL = "https://seeker-v6.com/personas/apiBasico/dni"
            HEADERS = {"Authorization": "Bearer sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"}
            try:
                r = requests.post(URL, headers=HEADERS, data={"dni": dni_input})
                st.session_state.res_v8 = r.json()
            except: st.error("Error de conexión")

# --- RESULTADOS ---
if "res_v8" in st.session_state:
    res = st.session_state.res_v8
    if res.get("status") == "success":
        raw = res.get("data", [])
        info = raw[0] if (isinstance(raw, list) and len(raw) > 0) else (raw if isinstance(raw, dict) else {})

        col_left, col_right = st.columns([1.8, 1])
        
        with col_left:
            st.markdown('<div class="premium-title">📝 Datos Obtenidos</div>', unsafe_allow_html=True)
            
            # Definimos los campos
            fields = [
                ("DNI / DOCUMENTO", ["dni", "numeroDocumento"]),
                ("NOMBRES", ["nombres", "nombre"]),
                ("APELLIDO PATERNO", ["ap_paterno", "paterno"]),
                ("APELLIDO MATERNO", ["ap_materno", "materno"]),
                ("CÓD. VERIF", ["digitoVerificacion", "codVerifica"]),
            ]
            
            # Construcción segura sin espacios que activen el modo código de markdown
            html = '<div class="data-card">'
            for label, keys in fields:
                valor = val(info, keys)
                # IMPORTANTE: Todo en una línea para evitar que Streamlit lo trate como bloque de código
                html += f'<div class="data-row"><div class="data-label">{label}</div><div class="data-value">{valor}</div></div>'
            html += '</div>'
            
            st.markdown(html, unsafe_allow_html=True)

        with col_right:
            st.markdown('<div style="color:#8b949e; font-size:11px; font-weight:bold; text-align:center; margin-bottom:10px;">BIOMETRÍA RENIEC</div>', unsafe_allow_html=True)
            st.markdown('<div class="photo-frame"><div class="no-photo-text">NO DISPONIBLE</div><div style="font-size:50px; margin-top:15px; opacity:0.3;">👤</div></div>', unsafe_allow_html=True)
else:
    st.info("Ingresa un DNI para comenzar")
