import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# 1. CONEXIÓN FIREBASE (CON LIMPIEZA DE LLAVE)
if not firebase_admin._apps:
    try:
        fb_dict = dict(st.secrets["firebase"])
        # Esto elimina problemas de saltos de línea mal pegados
        fb_dict["private_key"] = fb_dict["private_key"].replace("\\n", "\n")
        
        cred = credentials.Certificate(fb_dict)
        firebase_admin.initialize_app(cred)
    except Exception as e:
        st.error(f"Error de conexión: {e}")
        st.stop()

db = firestore.client()

# 2. CARGA DE LLAVES DE GOOGLE
try:
    G_ID = st.secrets["google_client_id"]
    G_SECRET = st.secrets["google_client_secret"]
except KeyError:
    st.error("Faltan las llaves de Google en Secrets.")
    st.stop()

# 3. INTERFAZ SEEKER v6
st.markdown("<style>.stApp { background: linear-gradient(135deg, #4facfe, #f093fb); }</style>", unsafe_allow_html=True)
st.title("SEEKER v6 - Login")

# Botón Google
url = f"https://accounts.google.com/o/oauth2/v2/auth?client_id={G_ID}&response_type=code&scope=openid%20email%20profile&redirect_uri=https://appappppy-43nnqkr6ctadmkdomd2nxc.streamlit.app/"
st.link_button("🌐 Ingresar con Google", url)

st.write("---")

# Login Manual ZATOCHY
u = st.text_input("Usuario").upper()
p = st.text_input("Contraseña", type="password")

if st.button("Ingresar"):
    res = db.collection("COLECCION").document(u).get()
    if res.exists and res.to_dict().get('PASSWORD') == p:
        st.success(f"Bienvenido {u}")
        st.session_state.user = res.to_dict()
    else:
        st.error("Credenciales inválidas.")
