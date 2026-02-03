import streamlit as st
import requests

# 1. Configuración de pantalla
st.set_page_config(page_title="Búsqueda Básica - Free", layout="wide")

# 2. CSS Estilo Knowlers (Tabla Azul)
st.markdown("""
<style>
    .stApp { background-color: #0b0e14; }
    .results-table-container { width: 100%; border-radius: 4px; overflow: hidden; border: 1px solid #1e293b; margin-top: 20px; }
    table { width: 100%; border-collapse: collapse; font-family: 'Inter', sans-serif; font-size: 11px; color: #cbd5e1; }
    thead tr { background-color: #0076ce !important; }
    th { color: white !important; text-align: left; padding: 12px 10px; text-transform: uppercase; font-weight: 700; border-right: 1px solid rgba(255,255,255,0.1); }
    tbody tr:nth-child(even) { background-color: #161b22; }
    tbody tr:nth-child(odd) { background-color: #0b0e14; }
    tbody tr:hover { background-color: #1c2533; }
    td { padding: 10px; border-bottom: 1px solid #1e293b; border-right: 1px solid #1e293b; }
    .dni-cell { color: #58a6ff; font-weight: bold; }
    .name-cell { color: #ffffff; font-weight: bold; }
    .premium-tag { color: #facc15; font-size: 9px; font-weight: bold; }
    #MainMenu, footer, header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

def fmt_free(d, k):
    # Campos que suelen venir en la API Básica
    basic_fields = ['dni', 'nombres', 'ap_paterno', 'ap_materno', 'edad', 'fec_nacimiento']
    v = d.get(k, "")
    
    if k not in basic_fields:
        return '<span class="premium-tag">💎 SOLO EN PREMIUM</span>'
        
    return str(v).upper() if v and str(v).strip() != "" else "-"

# --- PANEL LATERAL ---
with st.sidebar:
    st.markdown("<h2 style='text-align:center;'>🎁 CONSULTA GRATIS</h2>", unsafe_allow_html=True)
    n = st.text_input("NOMBRES", placeholder="alexander")
    p = st.text_input("AP. PATERNO", placeholder="ruiz")
    m = st.text_input("AP. MATERNO")
    
    st.markdown("---")
    c_e1, c_e2 = st.columns(2)
    with c_e1: e_min = st.text_input("EDAD MÍN", value="0")
    with c_e2: e_max = st.text_input("EDAD MÁX", value="100")
    
    if st.button("EJECUTAR CONSULTA GRATIS", type="primary", use_container_width=True):
        URL = "https://seeker-v6.com/personas/apiBasico/nombresApellidos"
        HEADERS = {"Authorization": "Bearer sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"}
        # NOTA: En la versión básica el parámetro es "nombres" en plural
        DATA = {"nombres": n, "paterno": p, "materno": m, "edadMin": e_min, "edadMax": e_max}
        try:
            with st.spinner("Buscando en base de datos gratuita..."):
                r = requests.post(URL, headers=HEADERS, data=DATA)
                res = r.json()
                if res.get("status") == "success":
                    st.session_state.free_data = res.get("data", [])
                    st.session_state.free_page = 0
                else: st.error("Sin resultados en versión gratuita")
        except: st.error("Error al conectar con la API")

# --- TABLA DE RESULTADOS ---
if "free_data" in st.session_state:
    data = st.session_state.free_data
    total = len(data)
    per_page = 20
    if "free_page" not in st.session_state: st.session_state.free_page = 0
    
    start = st.session_state.free_page * per_page
    end = start + per_page
    current_data = data[start:end]

    st.markdown(f"#### 🆓 Resultados Gratuitos ({total} registros)")

    out = '<div class="results-table-container"><table><thead><tr>'
    out += '<th>#</th><th>DNI</th><th>NOMBRE</th><th>AP PATERNO</th><th>AP MATERNO</th><th>EDAD</th>'
    out += '<th>FECHA NACI</th><th>PADRE</th><th>MADRE</th><th>ORIGEN</th></tr></thead><tbody>'

    for i, r in enumerate(current_data):
        out += f'<tr>'
        out += f'<td>{start + i + 1}</td>'
        out += f'<td class="dni-cell">{fmt_free(r, "dni")}</td>'
        out += f'<td class="name-cell">{fmt_free(r, "nombres")}</td>'
        out += f'<td>{fmt_free(r, "ap_paterno")}</td>'
        out += f'<td>{fmt_free(r, "ap_materno")}</td>'
        out += f'<td>{fmt_free(r, "edad")}</td>'
        out += f'<td>{fmt_free(r, "fec_nacimiento")}</td>'
        out += f'<td>{fmt_free(r, "padre")}</td>'
        out += f'<td>{fmt_free(r, "madre")}</td>'
        out += f'<td>{fmt_free(r, "origen")}</td>'
        out += '</tr>'
    
    out += "</tbody></table></div>"
    st.markdown(out, unsafe_allow_html=True)

    st.markdown(f"<div style='text-align:center; padding: 20px; color:#94a3b8;'>Página {st.session_state.free_page + 1} de {(total // per_page) + 1}</div>", unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns([1,1,2,1,1])
    with col2:
        if st.session_state.free_page > 0:
            if st.button("⬅️ ANTERIOR", use_container_width=True):
                st.session_state.free_page -= 1
                st.rerun()
    with col4:
        if (st.session_state.free_page + 1) * per_page < total:
            if st.button("SIGUIENTE ➡️", use_container_width=True):
                st.session_state.free_page += 1
                st.rerun()
else:
    st.info("Utiliza los filtros de la izquierda para realizar una consulta gratuita.")
