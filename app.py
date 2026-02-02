import streamlit as st

# Configuración de página con tema oscuro
st.set_page_config(page_title="DataAPI Dashboard", layout="wide", initial_sidebar_state="collapsed")

# CSS personalizado para imitar el diseño de tu imagen
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #262730;
        color: white;
        border: 1px solid #4a4a4a;
    }
    .stButton>button:hover {
        border-color: #ff4b4b;
        color: #ff4b4b;
    }
    .login-box {
        padding: 2rem;
        border-radius: 10px;
        background-color: #161b22;
        border: 1px solid #30363d;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

if 'autenticado' not in st.session_state:
    st.session_state['autenticado'] = False

def login():
    cols = st.columns([1, 2, 1])
    with cols[1]:
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        st.image("https://cdn-icons-png.flaticon.com/512/7081/7081162.png", width=80)
        st.title("DataAPI Login")
        
        user = st.text_input("Usuario")
        pw = st.text_input("Contraseña", type="password")
        
        if st.button("ACCEDER AL SISTEMA"):
            if user == "admin" and pw == "666":
                st.session_state['autenticado'] = True
                st.rerun()
            else:
                st.error("Credenciales no válidas")
        st.markdown('</div>', unsafe_allow_html=True)

if not st.session_state['autenticado']:
    login()
    st.stop()

# --- DISEÑO DEL PANEL CENTRAL (POST-LOGIN) ---
st.title("🚀 Panel de Control")
st.markdown("### Seleccione un módulo para iniciar la consulta")

# Simulamos las tarjetas de tu imagen
c1, c2, c3 = st.columns(3)

with c1:
    st.info("👤 **MÓDULO PERSONAS**")
    st.caption("DNI Premium, Básico, Nombres")
    if st.button("Ir a Personas"):
        st.switch_page("pages/1_👤_Personas.py")

with c2:
    st.info("📞 **MÓDULO TELÉFONOS**")
    st.caption("Búsqueda por celular y operador")
    st.button("Próximamente", disabled=True, key="tel")

with c3:
    st.info("🚗 **MÓDULO VEHICULAR**")
    st.caption("Placas, Licencias, SOAT")
    st.button("Próximamente", disabled=True, key="veh")
