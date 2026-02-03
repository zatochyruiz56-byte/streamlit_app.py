import streamlit as st
import requests

# 1. Configuración de pantalla
st.set_page_config(page_title="Búsqueda Premium - Knowlers", layout="wide")

# 2. CSS Corregido (Diseño Limpio)
st.markdown("""
<style>
    .stApp { background-color: #0b0e14; }
    
    /* Contenedor de Tabla */
    .results-table-container { 
        width: 100%; border-radius: 4px; overflow: hidden; 
        border: 1px solid #1e293b; margin-top: 20px;
    }
    
    table { width: 100%; border-collapse: collapse; font-family: 'Inter', sans-serif; font-size: 11px; color: #cbd5e1; }
    
    /* CABECERA AZUL ORIGINAL */
    thead tr { background-color: #0076ce !important; }
    th { 
        color: white !important; text-align: left; padding: 12px 10px; 
        text-transform: uppercase; font-weight: 700; border-right: 1px solid rgba(255,255,255,0.1);
    }
    
    /* FILAS */
    tbody tr:nth-child(even) { background-color: #161b22; }
    tbody tr:nth-child(odd) { background-color: #0b0e14; }
    tbody tr:hover { background-color: #1c2533; }
    td { padding: 10px; border-bottom: 1px solid #1e293b; border-right: 1px solid #1e293b; }

    .dni-cell { color: #58a6ff; font-weight: bold; }
    .name-cell { color: #ffffff; font-weight: bold; }
    
    /* Ocultar elementos de Streamlit */
    #MainMenu, footer, header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

def fmt(d, k):
    v = d.get(k, "")
    return str(v).upper() if v and str(v).strip() != "" else "-"

# --- PANEL DE CONTROL ---
with st.sidebar:
    st.markdown("<h2 style='text-align:center;'>🔍 FILTROS PRO</h2>", unsafe_allow_html=True)
    nombre = st.text_input("NOMBRES", placeholder="alexander")
    paterno = st.text_input("AP. PATERNO", placeholder="ruiz")
    materno = st.text_input("AP. MATERNO")
    
    st.markdown("---")
    st.markdown("<b>RANGO DE EDAD</b>", unsafe_allow_html=True)
    c_e1, c_e2 = st.columns(2)
    with c_e1: e_min = st.text_input("MÍN", value="0")
    with c_e2: e_max = st.text_input("MÁX", value="100")
    
    if st.button("BUSCAR AHORA", type="primary", use_container_width=True):
        URL = "https://seeker-v6.com/personas/apiPremium/nombres"
        HEADERS = {"Authorization": "Bearer sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"}
        DATA = {"name": nombre, "appPaterno": paterno, "appMaterno": materno, "edadMin": e_min, "edadMax": e_max}
        try:
            with st.spinner("Consultando API..."):
                r = requests.post(URL, headers=HEADERS, data=DATA)
                res = r.json()
                if res.get("status") == "success":
                    st.session_state.data_full = res.get("data", [])
                    st.session_state.page = 0
                else: st.error("No se encontraron resultados")
        except: st.error("Error de conexión con el servidor")

# --- VISUALIZACIÓN ---
if "data_full" in st.session_state:
    data = st.session_state.data_full
    total = len(data)
    per_page = 20
    
    if "page" not in st.session_state: st.session_state.page = 0
    
    total_pages = (total // per_page) + (1 if total % per_page > 0 else 0)
    start = st.session_state.page * per_page
    end = start + per_page
    current_data = data[start:end]

    st.markdown(f"#### 📋 Resultados de Búsqueda ({total} registros)")

    # TABLA CONSTRUIDA EN UNA SOLA VARIABLE PARA EVITAR EL ERROR DE "LETRAS BLANCAS"
    out = '<div class="results-table-container"><table><thead><tr>'
    out += '<th>#</th><th>DNI</th><th>NOMBRE</th><th>AP PATERNO</th><th>AP MATERNO</th><th>EDAD</th>'
    out += '<th>FECHA NACI</th><th>PADRE</th><th>MADRE</th><th>ORIGEN</th><th>ESTADO</th></tr></thead><tbody>'

    for i, r in enumerate(current_data):
        out += f'<tr>'
        out += f'<td>{start + i + 1}</td>'
        out += f'<td class="dni-cell">{fmt(r, "dni")}</td>'
        out += f'<td class="name-cell">{fmt(r, "nombres")}</td>'
        out += f'<td>{fmt(r, "ap_paterno")}</td>'
        out += f'<td>{fmt(r, "ap_materno")}</td>'
        out += f'<td>{fmt(r, "edad")}</td>'
        out += f'<td>{fmt(r, "fec_nacimiento")}</td>'
        out += f'<td>{fmt(r, "padre")}</td>'
        out += f'<td>{fmt(r, "madre")}</td>'
        out += f'<td>{fmt(r, "origen")}</td>'
        out += f'<td>{fmt(r, "estado_civil")}</td>'
        out += '</tr>'
    
    out += "</tbody></table></div>"
    st.markdown(out, unsafe_allow_html=True)

    # PAGINACIÓN LIMPIA
    st.markdown(f"<div style='text-align:center; padding: 20px; color:#94a3b8;'><b>Mostrando {start+1} a {min(end, total)} de {total}</b></div>", unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns([1,1,2,1,1])
    with col2:
        if st.session_state.page > 0:
            if st.button("⬅️ ANTERIOR", use_container_width=True):
                st.session_state.page -= 1
                st.rerun()
    with col4:
        if st.session_state.page < total_pages - 1:
            if st.button("SIGUIENTE ➡️", use_container_width=True):
                st.session_state.page += 1
                st.rerun()
else:
    st.info("Ingresa los nombres y pulsa BUSCAR para ver la tabla.")
