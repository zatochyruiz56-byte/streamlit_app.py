import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from httpx_oauth.clients.google import GoogleOAuth2

# 1. INICIALIZACIÓN DE FIREBASE
if not firebase_admin._apps:
    creds_dict = dict(st.secrets["firebase"])
    creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n")
    firebase_admin.initialize_app(credentials.Certificate(creds_dict))

db = firestore.client()

# 2. CONFIGURACIÓN DE GOOGLE OAUTH
client_id = st.secrets["google_client_id"]
client_secret = st.secrets["google_client_secret"]
redirect_uri = "https://appappppy-43nnqkr6ctadmkdomd2nxc.streamlit.app/"
client = GoogleOAuth2(client_id, client_secret)

# 3. INTERFAZ SEEKER V6
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #4facfe, #00f2fe, #f093fb); }
    .card { background: white; padding: 2rem; border-radius: 15px; color: #333; box-shadow: 0 10px 25px rgba(0,0,0,0.1); }
    </style>
""", unsafe_allow_html=True)

async def get_google_user(code):
    token = await client.get_access_token(code, redirect_uri)
    user_info = await client.get_id_email(token["access_token"])
    return user_info

# Lógica de navegación
if 'user' not in st.session_state: st.session_state.user = None

# Verificar si venimos regresando de Google
query_params = st.query_params
if "code" in query_params and not st.session_state.user:
    import asyncio
    user_info = asyncio.run(get_google_user(query_params["code"]))
    # Buscamos si el correo existe en tu COLECCION
    email = user_info[1]
    docs = db.collection("COLECCION").where("email", "==", email).stream()
    user_data = None
    for d in docs: user_data = d.to_dict()
    
    if user_data:
        st.session_state.user = user_data
        st.query_params.clear()
        st.rerun()
    else:
        st.error("Tu correo de Google no está registrado en el sistema.")

# --- VISTA DE LOGIN ---
if not st.session_state.user:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.title("Iniciar Sesión - SEEKER v6")
    
    # BOTÓN DE GOOGLE REAL
    authorization_url = asyncio.run(client.get_authorization_url(redirect_uri, scope=["email", "profile"]))
    st.link_button("🌐 Ingresar con Google", authorization_url)
    
    st.write("--- o entra con tu usuario ---")
    user_in = st.text_input("Usuario").upper()
    pass_in = st.text_input("Contraseña", type="password")
    
    if st.button("Ingresar"):
        doc = db.collection("COLECCION").document(user_in).get()
        if doc.exists:
            datos = doc.to_dict()
            if datos.get('PASSWORD') == pass_in:
                st.session_state.user = datos
                st.rerun()
            else: st.error("Contraseña incorrecta")
        else: st.error("El usuario no existe")
    st.markdown('</div>', unsafe_allow_html=True)
else:
    # PANEL PRINCIPAL
    st.sidebar.title(f"Hola, {st.session_state.user['USERNAME']}")
    st.sidebar.metric("Créditos", f"S/ {st.session_state.user['creditos']}")
    
    if st.sidebar.button("Cerrar Sesión"):
        st.session_state.user = None
        st.rerun()
    st.write("## Bienvenido al buscador")
