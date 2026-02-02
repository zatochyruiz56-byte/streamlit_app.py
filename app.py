import streamlit as st

st.set_page_config(page_title="DataAPI Dashboard", layout="wide")

# Login Simple
if 'autenticado' not in st.session_state:
    st.session_state['autenticado'] = False

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
                st.error("Credenciales incorrectas")
    st.stop()

# Dashboard
st.title("🚀 Panel de Control")
st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("👤 Personas")
    if st.button("ABRIR MÓDULO", key="btn_per"):
        # Probamos todas las combinaciones que Streamlit suele usar
        paginas = ["pages/Personas.py", "Personas.py", "pages/personas.py", "personas.py"]
        exito = False
        for p in paginas:
            try:
                st.switch_page(p)
                exito = True
                break
            except:
                continue
        
        if not exito:
            st.error("⚠️ Error de sistema: El servidor no reconoce la carpeta 'pages' todavía.")
            st.info("POR FAVOR: Haz clic en 'Manage App' -> 'Reboot App' para actualizar los archivos.")

with col2:
    st.subheader("📞 Teléfonos")
    st.button("PRÓXIMAMENTE", disabled=True, key="btn_tel")

with col3:
    st.subheader("🚗 Vehicular")
    st.button("PRÓXIMAMENTE", disabled=True, key="btn_veh")
