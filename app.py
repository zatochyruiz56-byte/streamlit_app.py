import streamlit as st

# Configuración básica
st.set_page_config(page_title="DataAPI Dashboard", layout="wide")

# Estilo para evitar errores de IDs duplicados (Imagen 492219)
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    .module-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# Login
if 'autenticado' not in st.session_state:
    st.session_state['autenticado'] = False

if not st.session_state['autenticado']:
    _, col, _ = st.columns([1, 1, 1])
    with col:
        st.title("🔐 Acceso")
        u = st.text_input("Usuario")
        p = st.text_input("Contraseña", type="password")
        if st.button("INGRESAR"):
            if u == "admin" and p == "666":
                st.session_state['autenticado'] = True
                st.rerun()
            else:
                st.error("Credenciales incorrectas")
    st.stop()

# Dashboard
st.title("🚀 Panel de Control")
st.markdown("---")

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown('<div class="module-card">', unsafe_allow_html=True)
    st.subheader("👤 Personas")
    # Intentamos la ruta directa. Si falla, Streamlit nos dirá por qué.
    if st.button("ABRIR MÓDULO", key="btn_p"):
        try:
            st.switch_page("pages/Personas.py")
        except Exception as e:
            st.error(f"No se encontró el archivo: pages/Personas.py. Verifique el nombre en GitHub.")
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="module-card">', unsafe_allow_html=True)
    st.subheader("📞 Teléfonos")
    st.button("PRÓXIMAMENTE", disabled=True, key="btn_t")
    st.markdown('</div>', unsafe_allow_html=True)

with c3:
    st.markdown('<div class="module-card">', unsafe_allow_html=True)
    st.subheader("🚗 Vehicular")
    st.button("PRÓXIMAMENTE", disabled=True, key="btn_v")
    st.markdown('</div>', unsafe_allow_html=True)
