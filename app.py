import streamlit as st

# Configuración de la página (Layout amplio y tema oscuro)
st.set_page_config(page_title="DataAPI Dashboard", layout="wide", initial_sidebar_state="collapsed")

# Estilo CSS para el diseño de tarjetas (Estilo Imagen 31)
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    .module-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 15px;
        padding: 25px;
        text-align: center;
        transition: 0.3s;
        margin-bottom: 20px;
    }
    .module-card:hover { border-color: #58a6ff; }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        background-color: #21262d;
        color: white;
        border: 1px solid #30363d;
    }
    .stButton>button:hover {
        border-color: #58a6ff;
        color: #58a6ff;
    }
    </style>
    """, unsafe_allow_html=True)

# Lógica de Autenticación
if 'autenticado' not in st.session_state:
    st.session_state['autenticado'] = False

if not st.session_state['autenticado']:
    cols = st.columns([1, 1, 1])
    with cols[1]:
        st.title("🔐 DataAPI Login")
        user = st.text_input("Usuario")
        pw = st.text_input("Contraseña", type="password")
        if st.button("ACCEDER AL SISTEMA"):
            # Cambia estas credenciales a tu gusto
            if user == "admin" and pw == "666":
                st.session_state['autenticado'] = True
                st.rerun()
            else:
                st.error("Usuario o clave incorrectos")
    st.stop()

# --- PANEL PRINCIPAL (POST-LOGIN) ---
st.title("🚀 Bienvenido al Panel de Consultas")
st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="module-card">', unsafe_allow_html=True)
    st.subheader("👤 Módulo Personas")
    st.caption("DNI Premium, Básico, Nombres, Padres")
    if st.button("INGRESAR", key="btn_personas"):
        # RUTA REPARADA: Apunta a la carpeta 'pages' y al archivo 'Personas.py'
        st.switch_page("pages/Personas.py")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="module-card">', unsafe_allow_html=True)
    st.subheader("📞 Módulo Telefonía")
    st.caption("Celulares, Operadores, Titulares")
    st.button("PRÓXIMAMENTE", disabled=True, key="btn_tel")
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="module-card">', unsafe_allow_html=True)
    st.subheader("🚗 Módulo Vehicular")
    st.caption("Placas, Licencias, SOAT")
    st.button("PRÓXIMAMENTE", disabled=True, key="btn_veh")
    st.markdown('</div>', unsafe_allow_html=True)
