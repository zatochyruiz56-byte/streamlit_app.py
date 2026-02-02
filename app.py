import streamlit as st

st.set_page_config(page_title="DataAPI", layout="wide")

if 'autenticado' not in st.session_state:
    st.session_state['autenticado'] = False

# --- LOGIN ---
if not st.session_state['autenticado']:
    _, col, _ = st.columns([1, 1, 1])
    with col:
        st.title("🔐 Acceso")
        u = st.text_input("Usuario")
        p = st.text_input("Clave", type="password")
        if st.button("INGRESAR"):
            if u == "admin" and p == "666":
                st.session_state['autenticado'] = True
                st.rerun()
            else:
                st.error("Error")
    st.stop()

# --- DASHBOARD ---
st.title("🚀 Panel de Control")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("👤 Personas")
    if st.button("ABRIR MÓDULO", key="btn_p"):
        # Intentamos las 3 formas posibles en que Streamlit lee archivos
        try:
            st.switch_page("pages/Personas.py")
        except:
            try:
                st.switch_page("Personas.py")
            except:
                st.error("Error de ruta. Por favor, haz REBOOT en Manage App.")

with col2:
    st.subheader("📞 Teléfonos")
    st.button("PRÓXIMAMENTE", key="btn_t", disabled=True)

with col3:
    st.subheader("🚗 Vehicular")
    st.button("PRÓXIMAMENTE", key="btn_v", disabled=True)
