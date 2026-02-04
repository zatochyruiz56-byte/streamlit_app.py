import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import asyncio
from httpx_oauth.clients.google import GoogleOAuth2

# --- 1. INICIALIZACIÓN DE FIREBASE ---
if not firebase_admin._apps:
    creds_dict = dict(st.secrets["firebase"])
    creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n")
    firebase_admin.initialize_app(credentials.Certificate(creds_dict))
db = firestore.client()

# --- 2. CONFIGURACIÓN GOOGLE ---
client_id = st.secrets["google_client_id"] # Esto ya no dará error
client_secret = st.secrets["google_client_secret"]
redirect_uri = "https://appappppy-43nnqkr6ctadmkdomd2nxc.streamlit.app/"
client = GoogleOAuth2(client_id, client_secret)

# --- 3. DISEÑO SEEKER v6 ---
st.markdown("<style>.stApp { background: linear-gradient(135deg, #4facfe, #f093fb); }</style>", unsafe_allow_html=True)

if 'user' not in st.session_state: st.session_state.user = None

# Lógica para capturar el regreso de Google
async def get_access_token(code):
    return await client.get_access_token(code, redirect_uri)

async def get_user_info(token):
    return await client.get_id_email(token)

params = st.query_params
if "code" in params:
    token = asyncio.run(get_access_token(params["code"]))
    user_id, email = asyncio.run(get_user_info(token["access_token"]))
    # Buscamos en tu colección COLECCION
    docs = db.collection("COLECCION").where("email", "==", email).get()
    if docs:
        st.session_state.user = docs[0].to_dict()
        st.query_params.clear()
        st.rerun()
    else:
        st.error("Correo no registrado. Usa el formulario de registro.")

# --- INTERFAZ DE LOGIN ---
if not st.session_state.user:
    st.title("Iniciar Sesión - SEEKER v6")
    
    # Botón Real de Google
    authorization_url = asyncio.run(client.get_authorization_url(redirect_uri, scope=["email", "profile"]))
    st.link_button("🌐 Ingresar con Google", authorization_url)
    
    st.write("--- o usa tu cuenta local ---")
    user_in = st.text_input("Usuario").upper()
    pass_in = st.text_input("Contraseña", type="password")
    
    if st.button("Ingresar"):
        doc = db.collection("COLECCION").document(user_in).get()
        if doc.exists and doc.to_dict().get('PASSWORD') == pass_in:
            st.session_state.user = doc.to_dict()
            st.rerun()
        else:
            st.error("Usuario o contraseña incorrectos")
            
    if st.button("¿No tienes cuenta? Regístrate"):
        st.info("Función de registro activada. Completa los campos.")
else:
    # PANEL PRINCIPAL
    st.sidebar.title(f"Hola, {st.session_state.user['USERNAME']}")
    st.sidebar.metric("Tus Créditos", f"S/ {st.session_state.user['creditos']}")
    if st.sidebar.button("Cerrar Sesión"):
        st.session_state.user = None
        st.rerun()
    st.write("## Bienvenido al sistema de búsqueda")
