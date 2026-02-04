import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# 1. Conexión segura a Firestore
if not firebase_admin._apps:
    # Usamos st.secrets["firebase"] porque definimos el bloque arriba
    creds = dict(st.secrets["firebase"])
    creds["private_key"] = creds["private_key"].replace("\\n", "\n")
    firebase_admin.initialize_app(credentials.Certificate(creds))

db = firestore.client()

# 2. Configuración de Google (Llamada directa)
try:
    # Estas líneas ya no fallarán si arreglaste los Secrets arriba
    G_CLIENT_ID = st.secrets["google_client_id"]
    G_CLIENT_SECRET = st.secrets["google_client_secret"]
except KeyError:
    st.error("Error: Las llaves de Google no se encuentran en Secrets.")
    st.stop()

# 3. Interfaz SEEKER v6
st.markdown("<style>.stApp { background: linear-gradient(135deg, #4facfe, #f093fb); }</style>", unsafe_allow_html=True)
st.title("Iniciar Sesión - SEEKER v6")

# Botón de Google con redirección real
redirect_url = f"https://accounts.google.com/o/oauth2/v2/auth?client_id={G_CLIENT_ID}&response_type=code&scope=openid%20email%20profile&redirect_uri=https://appappppy-43nnqkr6ctadmkdomd2nxc.streamlit.app/"

st.link_button("🌐 Ingresar con Google", redirect_url)

st.write("---")

# Login manual para ZATOCHY
user_in = st.text_input("Usuario").upper()
pass_in = st.text_input("Contraseña", type="password")

if st.button("Ingresar"):
    # Buscamos en la colección exacta de tu imagen
    doc = db.collection("COLECCION").document(user_in).get()
    if doc.exists:
        datos = doc.to_dict()
        if datos.get('PASSWORD') == pass_in:
            st.success(f"Bienvenido {datos.get('NAMES')}")
            st.session_state.user = datos
            # Aquí podrías redirigir al panel principal
        else:
            st.error("Contraseña incorrecta.")
    else:
        st.error("El usuario no existe.")
