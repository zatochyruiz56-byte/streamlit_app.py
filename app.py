import streamlit as st

st.set_page_config(page_title="DataAPI Dashboard", layout="wide")

# Estado de autenticación
if 'auth' not in st.session_state:
    st.session_state['auth'] = False

# --- IMAGEN 1 Y 2: LOGIN ---
if not st.session_state['auth']:
    _, col, _ = st.columns([1, 1, 1])
    with col:
        st.title("🔐 Acceso")
        user = st.text_input("Usuario")
        passw = st.text_input("Contraseña", type="password")
        if st.button("INGRESAR"):
            if user == "admin" and passw == "666":
                st.session_state['auth'] = True
                st.rerun()
            else:
                st.error("Credenciales incorrectas")
    st.stop()

# --- MENÚ PRINCIPAL ---
st.title("🚀 Panel de Control")
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.subheader("👤 Módulo Personas")
    if st.button("ABRIR BUSCADOR"):
        st.switch_page("pages/personas.py")

with col2:
    st.subheader("⚙️ Otros Módulos")
    st.info("Próximamente: Teléfonos y Vehículos")
