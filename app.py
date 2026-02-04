import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# 1. Configuración de página y estado (EVITA EL ATTRIBUTEERROR)
st.set_page_config(page_title="ZTCHY PRO", layout="centered")

if 'user' not in st.session_state:
    st.session_state.user = None

# 2. Inicialización de Firebase (RESISTENTE A ERRORES DE LLAVE PEM)
if not firebase_admin._apps:
    try:
        # Cargamos los secretos de la sección [firebase]
        secrets_dict = dict(st.secrets["firebase"])
        # Limpiamos posibles saltos de línea mal formateados
        secrets_dict["private_key"] = secrets_dict["private_key"].replace("\\n", "\n")
        
        cred = credentials.Certificate(secrets_dict)
        firebase_admin.initialize_app(cred)
    except Exception as e:
        st.error(f"Error crítico en Firebase: {e}")
        st.info("Asegúrate de haber guardado los Secrets con comillas triples.")
        st.stop()

db = firestore.client()

# 3. Interfaz de Login
if not st.session_state.user:
    st.title("🚀 ZTCHY PRO - Acceso")
    
    # Datos de Google
    client_id = st.secrets["google_client_id"]
    # Este link debe terminar en / para coincidir con tu consola
    redirect_uri = "https://appappppy-43nnqkr6ctadmkdomd2nxc.streamlit.app/"
    
    auth_url = (
        f"https://accounts.google.com/o/oauth2/v2/auth?"
        f"client_id={client_id}&"
        f"response_type=code&"
        f"scope=openid%20email%20profile&"
        f"redirect_uri={redirect_uri}&"
        f"prompt=select_account"
    )

    # Botón de Google que carga en la misma pestaña
    st.markdown(f"""
        <a href="{auth_url}" target="_self" style="
            text-decoration: none; display: block; text-align: center;
            padding: 12px; background-color: #4285F4; color: white;
            border-radius: 8px; font-weight: bold; margin: 20px 0;
        ">Entrar con Google</a>
    """, unsafe_allow_html=True)

    st.divider()
    
    # Acceso manual
    user_input = st.text_input("Usuario").upper()
    pass_input = st.text_input("Contraseña", type="password")
    
    if st.button("Ingresar", use_container_width=True):
        doc = db.collection("USUARIOS").document(user_input).get()
        if doc.exists and doc.to_dict().get("PASSWORD") == pass_input:
            st.session_state.user = doc.to_dict()
            st.rerun()
        else:
            st.error("Usuario o contraseña no válidos.")

# 4. Panel Principal
else:
    u = st.session_state.user
    st.sidebar.title(f"Bienvenido, {u.get('USERNAME', 'Usuario')}")
    if st.sidebar.button("Salir"):
        st.session_state.user = None
        st.rerun()
    
    st.header("🔎 Panel Seeker v6")
    st.write(f"Has iniciado sesión como: **{u.get('NAMES', 'Sin Nombre')}**")
