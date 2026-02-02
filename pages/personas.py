import streamlit as st
import requests

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(layout="wide", page_title="Consultas Pro")

# --- CSS PROFESIONAL (Estilo Seeker-V6) ---
st.markdown("""
    <style>
    .main { background-color: #0b0e14; }
    .stApp { background-color: #0b0e14; }
    
    /* Contenedor de búsqueda */
    .search-card {
        background: #161b22;
        border: 2px solid #2ea043;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 0 15px rgba(46, 160, 67, 0.2);
    }
    
    /* Tabla de resultados */
    .result-table {
        width: 100%;
        background: #161b22;
        border-collapse: collapse;
        border-radius: 8px;
        overflow: hidden;
    }
    .result-table td {
        padding: 12px;
        border-bottom: 1px solid #30363d;
        color: #c9d1d9;
    }
    .result-table td:first-child {
        font-weight: bold;
        color: #8b949e;
        width: 40%;
    }
    
    /* Header de Resultados */
    .res-header {
        color: #a371f7;
        font-size: 1.2rem;
        font-weight: bold;
        margin-bottom: 15px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    /* Imagen de perfil */
    .profile-frame {
        border: 4px solid #30363d;
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    </style>
""", unsafe_allow_html=True)

# --- LAYOUT DE TRES COLUMNAS ---
col_form, col_data, col_photo = st.columns([1.2, 2, 1.5], gap="medium")

with col_form:
    st.markdown('<div class="search-card">', unsafe_allow_html=True)
    st.markdown("### 💎 Consulta Premium")
    doc_type = st.tabs(["DNI", "NOMBRE", "PADRES", "FULL"])
    dni = st.text_input("NUMERO DOC*", placeholder="Ingrese DNI")
    if st.button("Buscar 🔍", use_container_width=True):
        # Lógica de tu API aquí...
        st.session_state.search_done = True
    st.markdown('</div>', unsafe_allow_html=True)

with col_data:
    st.markdown('<div class="res-header">✨ Resultados Pro <span style="color:white">knowlers.xyz</span></div>', unsafe_allow_html=True)
    
    # Simulación de datos de API (Cámbialo por r.json())
    data = {
        "DNI": "60799566 - 1",
        "Nombres": "JHORDINHO ZATOCHY",
        "Apellido Paterno": "RUIZ",
        "Apellido Materno": "CRUZ",
        "Fecha Nacimiento": "19/12/2005"
    }
    
    html_table = '<table class="result-table">'
    for k, v in data.items():
        html_table += f'<tr><td>{k}</td><td>{v}</td></tr>'
    html_table += '</table>'
    st.markdown(html_table, unsafe_allow_html=True)

with col_photo:
    st.markdown('<div class="profile-frame">', unsafe_allow_html=True)
    st.image("https://via.placeholder.com/400x500", use_container_width=True) # Usa la URL de tu API
    st.markdown('</div>', unsafe_allow_html=True)
