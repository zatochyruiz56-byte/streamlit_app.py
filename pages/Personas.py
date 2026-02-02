import streamlit as st

# 1. Configuración de página
st.set_page_config(page_title="DataAPI Dashboard", layout="wide", initial_sidebar_state="collapsed")

# 2. Estilo Dark
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

# 3. Lógica de Login
if 'autenticado' not in st.session_state:
    st.session_state['autenticado'] = False

if not st.session_state['autenticado']:
    _, col, _ = st.columns([1, 1, 1])
    with col:
        st.title("🔐 Acceso")
        user = st.text_input("Usuario")
        passw = st.text_input("Contraseña", type="password")
        if st.button("INGRESAR"):
            if user == "admin" and passw == "666":
                st.session_state['autenticado'] = True
                st.rerun()
            else:
                st.error("Credenciales incorrectas")
    st.stop()

# 4. Dashboard Principal
st.title("🚀 Panel de Control")
st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="module-card">', unsafe_allow_html=True)
    st.subheader("👤 Módulo Personas")
    # TRUCO: Usamos el nombre exacto que aparece en tu GitHub (Imagen 498e3c)
    if st.button("ABRIR MÓDULO", key="btn_p"):
        try:
            st.switch_page("pages/Personas.py")
        except:
            # Si falla con mayúscula, intentamos con minúscula por si acaso
            st.switch_page("pages/personas.py")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="module-card">', unsafe_allow_html=True)
    st.subheader("📞 Módulo Telefonía")
    st.button("PRÓXIMAMENTE", disabled=True, key="btn_t")
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="module-card">', unsafe_allow_html=True)
    st.subheader("🚗 Módulo Vehicular")
    st.button("PRÓXIMAMENTE", disabled=True, key="btn_v")
    st.markdown('</div>', unsafe_allow_html=True)
