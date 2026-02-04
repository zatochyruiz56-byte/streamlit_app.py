import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# 1. CONFIGURACIÓN DE PÁGINA Y ESTILO SEEKER v6
st.set_page_config(page_title="SEEKER v6", page_icon="🔍", layout="centered")

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 50%, #f093fb 100%);
    }
    .main-card {
        background: white;
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        color: #333;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background: linear-gradient(to right, #6a11cb, #2575fc);
        color: white;
        border: none;
    }
    </style>
""", unsafe_allow_html=True)

# 2. CONEXIÓN A TU BASE DE DATOS ZTCHY-PRO
if not firebase_admin._apps:
    creds_dict = dict(st.secrets["firebase"])
    creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n")
    cred = credentials.Certificate(creds_dict)
    firebase_admin.initialize_app(cred)

db = firestore.client()

# 3. MANEJO DE SESIÓN Y VISTAS
if 'page' not in st.session_state:
    st.session_state.page = 'login'
if 'user_data' not in st.session_state:
    st.session_state.user_data = None

# --- FUNCIÓN DE LOGIN ---
def login():
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.subheader("Iniciar Sesión - SEEKER v6")
    
    # Botón de Google (Interfaz)
    if st.button("🌐 Ingresar con Google"):
        st.info("Redirigiendo a Google...") 

    user_input = st.text_input("Nombre de Usuario", placeholder="Ej: ZATOCHY").upper()
    pass_input = st.text_input("Contraseña", type="password", placeholder="••••••••")

    if st.button("Ingresar"):
        # Buscamos en 'COLECCION' que es donde tienes a ZATOCHY
        doc_ref = db.collection("COLECCION").document(user_input).get()
        
        if doc_ref.exists:
            datos = doc_ref.to_dict()
            # El campo en tu Firestore es PASSWORD en mayúsculas
            if datos.get('PASSWORD') == pass_input:
                if datos.get('estado') == 'activo':
                    st.session_state.user_data = datos
                    st.session_state.page = 'home'
                    st.rerun()
                else:
                    st.error("🚫 Cuenta suspendida.")
            else:
                st.error("❌ Contraseña incorrecta.")
        else:
            st.error("❌ El usuario no existe.")

    if st.button("¿No tienes cuenta? Regístrate"):
        st.session_state.page = 'registro'
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- FUNCIÓN DE REGISTRO ---
def registro():
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.subheader("Crear Cuenta")
    
    new_user = st.text_input("Username").upper()
    new_name = st.text_input("Nombres y Apellidos")
    new_email = st.text_input("Correo Electrónico")
    new_pass = st.text_input("Contraseña", type="password")
    confirm_pass = st.text_input("Repetir Contraseña", type="password")

    if st.button("Finalizar Registro"):
        if new_pass != confirm_pass:
            st.error("Las contraseñas no coinciden")
        elif not new_user or not new_pass:
            st.error("Completa los campos obligatorios")
        else:
            # Creamos el documento en COLECCION
            db.collection("COLECCION").document(new_user).set({
                "USERNAME": new_user,
                "NAMES": new_name,
                "email": new_email,
                "PASSWORD": new_pass,
                "creditos": 0,
                "estado": "activo",
                "rol": "cliente"
            })
            st.success("✅ Registro exitoso. ¡Inicia sesión!")
            st.session_state.page = 'login'
            st.rerun()

    if st.button("Volver al Inicio"):
        st.session_state.page = 'login'
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- PANEL PRINCIPAL (HOME) ---
def home():
    user = st.session_state.user_data
    st.sidebar.title(f"Bienvenido, {user['USERNAME']}")
    st.sidebar.metric("Créditos Disponibles", f"S/ {user['creditos']}")
    
    if st.sidebar.button("Cerrar Sesión"):
        st.session_state.user_data = None
        st.session_state.page = 'login'
        st.rerun()

    st.title("🔍 Sistema de Consultas")
    st.write("Selecciona una opción en el menú de la izquierda.")

# --- NAVEGACIÓN ---
if st.session_state.page == 'login':
    login()
elif st.session_state.page == 'registro':
    registro()
elif st.session_state.page == 'home':
    home()
