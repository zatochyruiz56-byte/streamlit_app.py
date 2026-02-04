import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# Conexión con Secrets
if not firebase_admin._apps:
    creds_dict = dict(st.secrets["firebase"])
    creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n")
    cred = credentials.Certificate(creds_dict)
    firebase_admin.initialize_app(cred)

db = firestore.client()

# --- INTERFAZ SEEKER v6 ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #4facfe 0%, #00f2fe 50%, #f093fb 100%); }
    .card { background: white; padding: 2rem; border-radius: 15px; box-shadow: 0 10px 25px rgba(0,0,0,0.1); text-align: center; color: #333; }
    </style>
""", unsafe_allow_html=True)

if 'page' not in st.session_state: st.session_state.page = 'login'

# --- PÁGINA DE LOGIN ---
if st.session_state.page == 'login':
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Iniciar Sesión - SEEKER v6")
        
        # Simulación Login Google (Requiere configuración OAuth avanzada para ser real)
        if st.button("🌐 Ingresar con Google"):
            st.info("Configura la pantalla de consentimiento de Google Cloud para activar esto.")

        user_input = st.text_input("Nombre de Usuario", key="l_user").upper()
        pass_input = st.text_input("Contraseña", type="password", key="l_pass")

        if st.button("Ingresar"):
            # CORRECCIÓN: Buscamos en 'COLECCION'
            doc = db.collection("COLECCION").document(user_input).get()
            if doc.exists:
                res = doc.to_dict()
                if res['PASSWORD'] == pass_input:
                    st.success("¡Bienvenido!")
                    st.session_state.user = res
                    st.session_state.page = 'home'
                    st.rerun()
                else: st.error("Contraseña incorrecta")
            else: st.error("El usuario no existe")
        
        if st.button("¿No tienes cuenta? Regístrate"):
            st.session_state.page = 'registro'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# --- PÁGINA DE REGISTRO ---
elif st.session_state.page == 'registro':
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Crear Cuenta")
        new_user = st.text_input("Username", key="r_user").upper()
        new_names = st.text_input("Nombres y Apellidos")
        new_email = st.text_input("Correo")
        new_pass = st.text_input("Contraseña", type="password")
        
        if st.button("Finalizar Registro"):
            if new_user and new_pass:
                # Guardamos en la colección correcta
                db.collection("COLECCION").document(new_user).set({
                    "USERNAME": new_user,
                    "NAMES": new_names,
                    "email": new_email,
                    "PASSWORD": new_pass,
                    "creditos": 0,
                    "estado": "activo",
                    "rol": "cliente"
                })
                st.success("¡Registro exitoso! Ya puedes iniciar sesión.")
                st.session_state.page = 'login'
                st.rerun()
        
        if st.button("Volver al Login"):
            st.session_state.page = 'login'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# --- PÁGINA PRINCIPAL ---
elif st.session_state.page == 'home':
    st.sidebar.title(f"Hola, {st.session_state.user['USERNAME']}")
    st.sidebar.metric("Tus Créditos", f"S/ {st.session_state.user['creditos']}")
    if st.sidebar.button("Cerrar Sesión"):
        st.session_state.page = 'login'
        st.rerun()
    st.write("### Bienvenido al sistema de consultas")
