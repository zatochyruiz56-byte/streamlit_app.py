import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# 1. CONEXIÓN A TU BASE DE DATOS ZTCHY-PRO
if not firebase_admin._apps:
    creds_dict = dict(st.secrets["firebase"])
    creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n")
    cred = credentials.Certificate(creds_dict)
    firebase_admin.initialize_app(cred)

db = firestore.client()

# 2. DISEÑO SEEKER V6 (Inyectando el estilo de la imagen)
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 50%, #f093fb 100%);
    }
    .login-card {
        background: white;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        text-align: center;
        max-width: 400px;
        margin: auto;
    }
    </style>
""", unsafe_allow_html=True)

# 3. LÓGICA DE LOGIN
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    with st.container():
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        st.image("https://rotulosmatesanz.com/wp-content/uploads/2017/09/2000px-Google_G_Logo.svg_.png", width=30)
        st.subheader("Iniciar Sesión - SEEKER v6")
        
        user = st.text_input("Nombre de Usuario", placeholder="Ej: ZATOCHY")
        pw = st.text_input("Contraseña", type="password")
        
        if st.button("Ingresar"):
            # Buscamos el documento exacto que creaste en Firestore
            doc_ref = db.collection("USUARIOS").document(user.upper()).get()
            if doc_ref.exists:
                datos = doc_ref.to_dict()
                if datos.get("password") == pw:
                    if datos.get("estado") == "activo":
                        st.session_state.logged_in = True
                        st.session_state.user_data = datos
                        st.rerun()
                    else:
                        st.error("🚫 Estás BANEADO. Contacta al admin.")
                else:
                    st.error("❌ Contraseña incorrecta.")
            else:
                st.error("❌ El usuario no existe.")
        st.markdown('</div>', unsafe_allow_html=True)
else:
    # AQUÍ VA TU MENÚ DE CONSULTAS (DNI, LICENCIA, ETC)
    st.sidebar.success(f"Usuario: {st.session_state.user_data['username']}")
    st.sidebar.info(f"Créditos: S/ {st.session_state.user_data['creditos']}")
    
    if st.sidebar.button("Cerrar Sesión"):
        st.session_state.logged_in = False
        st.rerun()
        
    st.title("Bienvenido al Panel de Consultas")
