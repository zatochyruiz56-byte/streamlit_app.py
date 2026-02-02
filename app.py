import streamlit as st
import os

# Configuración de página
st.set_page_config(page_title="DataAPI Dashboard", layout="wide")

# Lógica de Login básica
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

# --- PANEL DE CONTROL ---
st.title("🚀 Panel de Control")
st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("👤 Módulo Personas")
    if st.button("ABRIR MÓDULO", key="btn_personas"):
        # Intentamos varias rutas por si Streamlit está confundido
        rutas_posibles = ["pages/Personas.py", "Personas.py", "pages/personas.py"]
        success = False
        for ruta in rutas_posibles:
            try:
                st.switch_page(ruta)
                success = True
                break
            except:
                continue
        
        if not success:
            st.error("⚠️ Error crítico: Streamlit no detecta el archivo en la carpeta 'pages'.")
            st.info("Sugerencia: Haz clic en 'Manage App' -> 'Reboot App' en el menú de Streamlit.")

with col2:
    st.subheader("📞 Teléfonos")
    st.button("PRÓXIMAMENTE", disabled=True, key="btn_tel")

with col3:
    st.subheader("🚗 Vehicular")
    st.button("PRÓXIMAMENTE", disabled=True, key="btn_veh")
