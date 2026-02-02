import streamlit as st

st.set_page_config(page_title="DataAPI Dashboard", layout="wide", initial_sidebar_state="collapsed")

# Estilo visual moderno
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    .module-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 15px;
        padding: 25px;
        text-align: center;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

if 'autenticado' not in st.session_state:
    st.session_state['autenticado'] = False

if not st.session_state['autenticado']:
    cols = st.columns([1, 1, 1])
    with cols[1]:
        st.title("🔐 Login")
        user = st.text_input("Usuario")
        pw = st.text_input("Contraseña", type="password")
        if st.button("INGRESAR"):
            if user == "admin" and pw == "666":
                st.session_state['autenticado'] = True
                st.rerun()
            else:
                st.error("Error de acceso")
    st.stop()

st.title("🚀 Panel de Control")
st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="module-card">', unsafe_allow_html=True)
    st.subheader("👤 Personas")
    if st.button("ABRIR MÓDULO", key="btn_per"):
        # ESTA RUTA DEBE COINCIDIR CON EL NOMBRE DEL ARCHIVO EN GITHUB
        st.switch_page("pages/Personas.py")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="module-card">', unsafe_allow_html=True)
    st.subheader("📞 Teléfonos")
    st.button("PRÓXIMAMENTE", disabled=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="module-card">', unsafe_allow_html=True)
    st.subheader("🚗 Vehicular")
    st.button("PRÓXIMAMENTE", disabled=True)
    st.markdown('</div>', unsafe_allow_html=True)
