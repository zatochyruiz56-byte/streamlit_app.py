import streamlit as st
import requests

# 1. Configuración de página
st.set_page_config(page_title="Buscador DNI - Estilo Premium", layout="wide")

# 2. CSS Calcado a la versión Premium
st.markdown("""
<style>
    .stApp { background-color: #0e1117; }
    
    /* Título con Icono */
    .premium-title {
        color: #00a36c;
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    /* Contenedor Principal de la Tabla */
    .data-card {
        background-color: #161b22;
        border-radius: 8px;
        border: 1px solid #30363d;
        overflow: hidden;
    }

    /* Filas de la Tabla */
    .data-row {
        display: flex;
        border-bottom: 1px solid #30363d;
        padding: 15px 20px;
        align-items: center;
    }
    .data-row:last-child { border-bottom: none; }

    /* Etiquetas (Grises, Pequeñas, Negrita) */
    .data-label {
        width: 40%;
        color: #8b949e;
        font-size: 11px;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }

    /* Valores (Blancos, Grandes, Negrita) */
    .data-value {
        width: 60%;
        color: #ffffff;
        font-weight: 700;
        font-size: 14px;
    }

    /* Foto/Biometría */
    .photo-label {
        text-align: center;
        color: #8b949e;
        font-size: 11px;
        font-weight: bold;
        margin-bottom: 10px;
        letter-spacing: 1px;
    }
    .photo-frame {
        border: 4px solid #30363d;
        border-radius: 15px;
        padding: 20px;
        background: #161b22;
        text-align: center;
        min-height: 250px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    .no-photo-text {
        color: #8b949e;
        font-size: 14px;
        font-weight: bold;
    }

    /* Ocultar elementos de Streamlit */
    #MainMenu, footer, header {visibility: hidden;}
    .stButton>button { border-radius: 8px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

def val(d, keys):
    if not isinstance(d, dict): return "N/D"
    for k in keys:
        v = d.get(k)
        if v and str(v).strip().lower() not in ["none", "null", ""]:
            return str(v).upper()
    return "N/D"

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
                st.session_state.res_basico = r.json()
            except Exception as e:
                st.error(f"Error: {e}")

    if st.button("🏠 MENÚ PRINCIPAL", use_container_width=True):
        st.switch_page("app.py")

# --- ÁREA DE RESULTADOS ---
if "res_basico" in st.session_state:
    res = st.session_state.res_basico
    if res.get("status") == "success":
        raw = res.get("data", [])
        info = raw[0] if (isinstance(raw, list) and len(raw) > 0) else (raw if isinstance(raw, dict) else {})

        c1, c2 = st.columns([1.8, 1])
        
        with c1:
            st.markdown('<div class="premium-title">📋 Datos Obtenidos</div>', unsafe_allow_html=True)
            
            # Los campos se muestran en el orden de tu captura
            items = [
                ("DNI / DOCUMENTO", ["dni", "numeroDocumento"]),
                ("NOMBRES", ["nombres", "nombre"]),
                ("APELLIDO PATERNO", ["ap_paterno", "paterno"]),
                ("APELLIDO MATERNO", ["ap_materno", "materno"]),
                ("CÓD. VERIF", ["digitoVerificacion", "codVerifica"]),
            ]
            
            # Construcción de la tabla Premium
            tabla_html = '<div class="data-card">'
            for label, keys in items:
                valor = val(info, keys)
                tabla_html += f"""
                <div class="data-row">
                    <div class="data-label">{label}</div>
                    <div class="data-value">{valor}</div>
                </div>
                """
            tabla_html += '</div>'
            st.markdown(tabla_html, unsafe_allow_html=True)

        with c2:
            st.markdown('<div class="photo-label">BIOMETRÍA RENIEC</div>', unsafe_allow_html=True)
            # Como pediste, aquí solo va "No disponible"
            st.markdown("""
            <div class="photo-frame">
                <div class="no-photo-text">NO DISPONIBLE</div>
                <div style="color: #30363d; margin-top: 10px; font-size: 40px;">👤</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.error("No se encontraron resultados.")
else:
    st.info("Esperando consulta...")
