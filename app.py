import streamlit as st

st.set_page_config(page_title="Sistema de Consultas", layout="centered")

# Inicializar el estado de autenticación
if 'autenticado' not in st.session_state:
    st.session_state['autenticado'] = False

def login():
    st.title("🔐 Acceso Protegido")
    with st.form("credenciales"):
        usuario = st.text_input("Usuario")
        clave = st.text_input("Contraseña", type="password")
        entrar = st.form_submit_button("Ingresar")
        
        if entrar:
            # Puedes cambiar 'admin' y '666' por lo que prefieras
            if usuario == "admin" and clave == "666":
                st.session_state['autenticado'] = True
                st.success("Acceso concedido")
                st.rerun()
            else:
                st.error("Usuario o clave incorrectos")

if not st.session_state['autenticado']:
    login()
    st.stop()

# Si está logueado, verá esto:
st.success("✅ Bienvenido al Panel Central")
st.info("Utilice el menú de la izquierda para navegar por los diferentes módulos.")
