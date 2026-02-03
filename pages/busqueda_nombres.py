import streamlit as st
import requests

# 1. Configuración
st.set_page_config(page_title="Búsqueda Premium - Debug Mode", layout="wide")

# 2. Estilo Premium
st.markdown("""
<style>
    .stApp { background-color: #0e1117; }
    .premium-title { color: #00a36c; font-size: 24px; font-weight: bold; margin-bottom: 20px; }
    .data-card { background-color: #161b22; border-radius: 8px; border: 1px solid #30363d; overflow: hidden; margin-bottom: 20px; }
    .data-row { display: flex; border-bottom: 1px solid #30363d; padding: 12px 20px; align-items: center; background-color: #161b22; }
    .data-row:last-child { border-bottom: none; }
    .data-label { width: 40%; color: #8b949e; font-size: 11px; font-weight: 800; text-transform: uppercase; }
    .data-value { width: 60%; color: #ffffff; font-weight: 700; font-size: 14px; }
    .photo-frame { border: 2px solid #30363d; border-radius: 12px; padding: 30px; background: #161b22; text-align: center; }
    #MainMenu, footer, header {visibility: hidden;}
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
    st.markdown("### 🔍 FILTROS")
    name = st.text_input("NOMBRES")
    pat = st.text_input("AP. PATERNO")
    mat = st.text_input("AP. MATERNO")
    e1 = st.text_input("EDAD MÍN", "0")
    e2 = st.text_input("EDAD MÁX", "100")
    
    if st.button("BUSCAR", type="primary", use_container_width=True):
        URL = "https://seeker-v6.com/personas/apiPremium/nombres"
        HEADERS = {"Authorization": "Bearer sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"}
        DATA = {"name": name, "appPaterno": pat, "appMaterno": mat, "edadMin": e1, "edadMax": e2}
        try:
            r = requests.post(URL, headers=HEADERS, data=DATA)
            st.session_state.raw_res = r.json()
        except: st.error("Error API")

# --- RESULTADOS ---
if "raw_res" in st.session_state:
    res = st.session_state.raw_res
    
    # --- SECCIÓN DE DEBUG (ESTO ES LO QUE NECESITAS VER) ---
    with st.expander("🛠️ VER INFORMACIÓN CRUDA (JSON COMPLETO)"):
        st.write("Copia este contenido y dime qué campos quieres agregar:")
        st.json(res)
    
    if res.get("status") == "success":
        data = res.get("data", [])
        st.markdown(f'<div class="premium-title">👥 Resultados: {len(data)}</div>', unsafe_allow_html=True)
        
        for p in data:
            c1, c2 = st.columns([2, 1])
            with c1:
                html = '<div class="data-card">'
                # Estos son los campos actuales, dime cuáles más del JSON quieres aquí:
                fields = [("DNI", ["dni"]), ("NOMBRES", ["nombres"]), ("PATERNO", ["paterno", "appPaterno"]), ("MATERNO", ["materno", "appMaterno"])]
                for lbl, ks in fields:
                    v = val(p, ks)
                    html += f'<div class="data-row"><div class="data-label">{lbl}</div><div class="data-value">{v}</div></div>'
                html += '</div>'
                st.markdown(html, unsafe_allow_html=True)
            with c2:
                st.markdown('<div class="photo-frame"><div style="color:#8b949e; font-weight:bold;">SIN FOTO</div></div>', unsafe_allow_html=True)
            st.markdown("---")
