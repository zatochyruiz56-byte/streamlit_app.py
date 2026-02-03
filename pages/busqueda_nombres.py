import streamlit as st
import requests

# 1. Configuración de página
st.set_page_config(page_title="Búsqueda Premium - Resultados Full", layout="wide")

# 2. Estilos CSS Premium (Diseño de Tabla y Cajones)
st.markdown("""
<style>
    .stApp { background-color: #0e1117; }
    .premium-header { 
        background: linear-gradient(90deg, #161b22 0%, #0d1117 100%);
        padding: 20px; border-radius: 12px; border: 1px solid #30363d; margin-bottom: 25px;
        display: flex; justify-content: space-between; align-items: center;
    }
    .count-badge { background: #238636; color: white; padding: 4px 12px; border-radius: 20px; font-weight: bold; font-size: 14px; }
    
    /* Contenedor de Persona */
    .person-card { 
        background-color: #161b22; border: 1px solid #30363d; border-radius: 12px; 
        margin-bottom: 20px; padding: 0; overflow: hidden; 
    }
    .card-header { background: #21262d; padding: 10px 20px; border-bottom: 1px solid #30363d; color: #58a6ff; font-weight: bold; font-size: 13px; }
    
    .data-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1px; background-color: #30363d; }
    .data-item { background-color: #161b22; padding: 12px 20px; }
    .data-label { color: #8b949e; font-size: 10px; font-weight: 800; text-transform: uppercase; margin-bottom: 4px; }
    .data-value { color: #ffffff; font-weight: 700; font-size: 13px; }
    
    /* Paginación */
    .nav-container { display: flex; justify-content: center; align-items: center; gap: 20px; margin-top: 30px; padding: 20px; }
    
    #MainMenu, footer, header {visibility: hidden;}
    .stButton>button { border-radius: 8px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# Helper para limpiar datos
def get_v(d, k, label="N/D"):
    val = d.get(k, "")
    if val is None or str(val).strip() == "" or str(val).lower() == "none":
        return label
    return str(val).upper()

# --- SIDEBAR FILTROS ---
with st.sidebar:
    st.markdown("<h2 style='text-align:center;'>🔍 FILTROS</h2>", unsafe_allow_html=True)
    nombres = st.text_input("NOMBRES")
    paterno = st.text_input("AP. PATERNO")
    materno = st.text_input("AP. MATERNO")
    
    if st.button("EJECUTAR CONSULTA", type="primary", use_container_width=True):
        if nombres or paterno:
            URL = "https://seeker-v6.com/personas/apiPremium/nombres"
            HEADERS = {"Authorization": "Bearer sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"}
            DATA = {"name": nombres, "appPaterno": paterno, "appMaterno": materno, "edadMin": "0", "edadMax": "100"}
            try:
                r = requests.post(URL, headers=HEADERS, data=DATA)
                res = r.json()
                if res.get("status") == "success":
                    st.session_state.all_results = res.get("data", [])
                    st.session_state.current_page = 0 # Reiniciar a página 1
                else: st.error("Error en API")
            except: st.error("Error de conexión")

# --- LÓGICA DE PAGINACIÓN ---
if "all_results" in st.session_state:
    data = st.session_state.all_results
    total = len(data)
    per_page = 20
    
    if "current_page" not in st.session_state:
        st.session_state.current_page = 0
        
    start_idx = st.session_state.current_page * per_page
    end_idx = start_idx + per_page
    page_data = data[start_idx:end_idx]
    total_pages = (total // per_page) + (1 if total % per_page > 0 else 0)

    # Header de Resultados
    st.markdown(f"""
    <div class="premium-header">
        <div style="color:white; font-size:20px; font-weight:bold;">👥 Resultados de Búsqueda</div>
        <div class="count-badge">TOTAL: {total} PERSONAS</div>
    </div>
    """, unsafe_allow_html=True)

    # Renderizar cada persona
    for i, p in enumerate(page_data):
        # Mapeo de todos los campos que vimos en tu JSON
        card_html = f"""
        <div class="person-card">
            <div class="card-header">REGISTRO #{start_idx + i + 1} - DOCUMENTO: {get_v(p, 'dni')}</div>
            <div class="data-grid">
                <div class="data-item"><div class="data-label">Nombres</div><div class="data-value">{get_v(p, 'nombres')}</div></div>
                <div class="data-item"><div class="data-label">Apellido Paterno</div><div class="data-value">{get_v(p, 'ap_paterno')}</div></div>
                <div class="data-item"><div class="data-label">Apellido Materno</div><div class="data-value">{get_v(p, 'ap_materno')}</div></div>
                
                <div class="data-item"><div class="data-label">Edad</div><div class="data-value">{get_v(p, 'edad')} AÑOS</div></div>
                <div class="data-item"><div class="data-label">Fecha Nacimiento</div><div class="data-value">{get_v(p, 'fec_nacimiento')}</div></div>
                <div class="data-item"><div class="data-label">Estado Civil</div><div class="data-value">{get_v(p, 'estado_civil')}</div></div>
                
                <div class="data-item"><div class="data-label">Padre</div><div class="data-value">{get_v(p, 'padre')}</div></div>
                <div class="data-item"><div class="data-label">Madre</div><div class="data-value">{get_v(p, 'madre')}</div></div>
                <div class="data-item"><div class="data-label">Género</div><div class="data-value">{'MASCULINO' if get_v(p, 'género') == '1' else 'FEMENINO'}</div></div>
                
                <div class="data-item" style="grid-column: span 3;"><div class="data-label">Origen</div><div class="data-value">{get_v(p, 'origen')}</div></div>
                <div class="data-item" style="grid-column: span 3;"><div class="data-label">Dirección Actual</div><div class="data-value">{get_v(p, 'dirección')}</div></div>
            </div>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)

    # BOTONES DE NAVEGACIÓN
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if st.session_state.current_page > 0:
            if st.button("⬅️ ANTERIOR", use_container_width=True):
                st.session_state.current_page -= 1
                st.rerun()
    
    with col2:
        st.markdown(f"<div style='text-align:center; color:#8b949e; font-weight:bold; padding-top:10px;'>PÁGINA {st.session_state.current_page + 1} DE {total_pages}</div>", unsafe_allow_html=True)
    
    with col3:
        if st.session_state.current_page < total_pages - 1:
            if st.button("SIGUIENTE ➡️", use_container_width=True):
                st.session_state.current_page += 1
                st.rerun()
else:
    st.info("Ingresa los datos en el panel izquierdo para comenzar la búsqueda premium.")
