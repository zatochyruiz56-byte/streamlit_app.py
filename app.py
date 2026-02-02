import streamlit as st

# Configuración de página
st.set_page_config(page_title="DataAPI Dashboard", layout="wide", initial_sidebar_state="collapsed")

# Estilo Dark Premium
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    .module-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 15px;
        padding: 25px;
        text-align: center;
        margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

if 'autenticado' not in st.session_state:
    st.session_state['autenticado'] = False

# Sistema de Login
if not st.session_state['autenticado']:
    cols = st.columns([1, 1, 1])
    with cols[1]:
        st.title("🔐 Acceso")
        u = st.text_input("Usuario")
        p = st.text_input("Clave", type="password")
        if st.button("INGRESAR"):
            if u == "admin" and p == "666":
                st.session_state['autenticado'] = True
                st.rerun()
            else:
                st.error("Credenciales incorrectas")
    st.stop()

# --- DASHBOARD ---
st.title("🚀 Panel de Control")
st.markdown("---")

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown('<div class="module-card">', unsafe_allow_html=True)
    st.subheader("👤 Personas")
    if st.button("ABRIR MÓDULO", key="btn_p"):
        # USAMOS EL NOMBRE SIMPLE SIN EMOJIS
        st.switch_page("pages/Personas.py")
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="module-card">', unsafe_allow_html=True)
    st.subheader("📞 Teléfonos")
    # Añadimos key="t1" para evitar el error DuplicateElementId
    st.button("PRÓXIMAMENTE", disabled=True, key="t1")
    st.markdown('</div>', unsafe_allow_html=True)

with c3:
    st.markdown('<div class="module-card">', unsafe_allow_html=True)
    st.subheader("🚗 Vehicular")
    # Añadimos key="v1" para evitar el error DuplicateElementId
    st.button("PRÓXIMAMENTE", disabled=True, key="v1")
    st.markdown('</div>', unsafe_allow_html=True)
