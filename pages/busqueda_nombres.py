import streamlit as st
import requests

# 1. Configuración de pantalla completa
st.set_page_config(page_title="Búsqueda Premium - Knowlers Style", layout="wide")

# 2. CSS para replicar la tabla azul original
st.markdown("""
<style>
    .stApp { background-color: #0b0e14; }
    
    /* Contenedor de Tabla */
    .table-container { width: 100%; overflow-x: auto; margin-top: 20px; border-radius: 4px; border: 1px solid #1e293b; }
    
    table { width: 100%; border-collapse: collapse; font-family: 'Inter', sans-serif; font-size: 12px; }
    
    /* Cabecera Azul Original */
    th { 
        background-color: #0076ce; color: white; text-align: left; 
        padding: 12px 10px; text-transform: uppercase; font-weight: 700;
        border-right: 1px solid rgba(255,255,255,0.1);
    }
    
    /* Filas */
    td { padding: 10px; border-bottom: 1px solid #1e293b; color: #cbd5e1; }
    tr:nth-child(even) { background-color: #161b22; }
    tr:hover { background-color: #1c2533; }

    /* Tags */
    .badge-dni { color: #58a6ff; font-weight: bold; }
    .badge-name { color: #ffffff; font-weight: 500; }
    
    /* Paginación */
    .page-info { text-align: center; color: #94a3b8; font-weight: bold; margin: 20px 0; }
    
    #MainMenu, footer, header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

def val(d, k):
    v = d.get(k, "")
    return str(v).upper() if v and str(v).strip() != "" else "-"

# --- PANEL LATERAL ---
with st.sidebar:
    st.markdown("<h2 style='text-align:center;'>🔍 CONSULTA PREMIUM</h2>", unsafe_allow_html=True)
    n = st.text_input("NOMBRES", placeholder="Ej: Alexander")
    p = st.text_input("AP. PATERNO", placeholder="Ej: Ruiz")
    m = st.text_input("AP. MATERNO")
    
    st.markdown("---")
    col_e1, col_e2 = st.columns(2)
    with col_e1: e_min = st.text_input("EDAD MÍN", value="0")
    with col_e2: e_max = st.text_input("EDAD MÁX", value="100")
    
    if st.button("BUSCAR AHORA", type="primary", use_container_width=True):
        URL = "https://seeker-v6.com/personas/apiPremium/nombres"
        HEADERS = {"Authorization": "Bearer sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"}
        DATA = {"name": n, "appPaterno": p, "appMaterno": m, "edadMin": e_min, "edadMax": e_max}
        try:
            r = requests.post(URL, headers=HEADERS, data=DATA)
            res = r.json()
            if res.get("status") == "success":
                st.session_state.data_full = res.get("data", [])
                st.session_state.page = 0
            else: st.error("Sin resultados")
        except: st.error("Error en API")

# --- ÁREA DE RESULTADOS ---
if "data_full" in st.session_state:
    data = st.session_state.data_full
    total = len(data)
    per_page = 20
    
    if "page" not in st.session_state: st.session_state.page = 0
    
    total_pages = (total // per_page) + (1 if total % per_page > 0 else 0)
    start = st.session_state.page * per_page
    end = start + per_page
    current_data = data[start:end]

    st.markdown(f"### 📊 Resultados Pro ({total} registros)")

    # Construcción manual de la tabla para evitar errores de renderizado
    table_html = """<div class="table-container"><table><thead><tr>
        <th>#</th><th>DNI</th><th>NOMBRE</th><th>AP PATERNO</th><th>AP MATERNO</th>
        <th>EDAD</th><th>FECHA NACI</th><th>PADRE</th><th>MADRE</th><th>ORIGEN</th><th>ESTADO</th>
    </tr></thead><tbody>"""

    for i, row in enumerate(current_data):
        idx = start + i + 1
        table_html += f"""
        <tr>
            <td>{idx}</td>
            <td class="badge-dni">{val(row, 'dni')}</td>
            <td class="badge-name">{val(row, 'nombres')}</td>
            <td>{val(row, 'ap_paterno')}</td>
            <td>{val(row, 'ap_materno')}</td>
            <td>{val(row, 'edad')}</td>
            <td>{val(row, 'fec_nacimiento')}</td>
            <td>{val(row, 'padre')}</td>
            <td>{val(row, 'madre')}</td>
            <td>{val(row, 'origen')}</td>
            <td>{val(row, 'estado_civil')}</td>
        </tr>
        """
    
    table_html += "</tbody></table></div>"
    st.markdown(table_html, unsafe_allow_html=True)

    # NAVEGACIÓN
    st.markdown(f'<div class="page-info">Mostrando {start+1}-{min(end, total)} de {total}</div>', unsafe_allow_html=True)
    
    c1, c2, c3, c4, c5 = st.columns([1,1,2,1,1])
    with c2:
        if st.session_state.page > 0:
            if st.button("⬅️ ANTERIOR", use_container_width=True):
                st.session_state.page -= 1
                st.rerun()
    with c4:
        if st.session_state.page < total_pages - 1:
            if st.button("SIGUIENTE ➡️", use_container_width=True):
                st.session_state.page += 1
                st.rerun()
else:
    st.info("👋 Realiza una búsqueda para ver los datos en formato tabla.")
