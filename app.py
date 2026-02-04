import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import requests
from urllib.parse import urlencode

# 1. Configuración de página y estado
st.set_page_config(page_title="ZTCHY PRO", layout="centered")

if 'user' not in st.session_state:
    st.session_state.user = None

# 2. Inicialización de Firebase
if not firebase_admin._apps:
    try:
        secrets_dict = dict(st.secrets["firebase"])
        secrets_dict["private_key"] = secrets_dict["private_key"].replace("\\n", "\n")
        cred = credentials.Certificate(secrets_dict)
        firebase_admin.initialize_app(cred)
    except Exception as e:
        st.error(f"Error crítico en Firebase: {e}")
        st.stop()

db = firestore.client()

# 3. Datos de Google OAuth
CLIENT_ID = st.secrets["google_client_id"]
CLIENT_SECRET = st.secrets["google_client_secret"]
REDIRECT_URI = "https://appappppy-43nnqkr6ctadmkdomd2nxc.streamlit.app/"

# 4. MANEJAR CALLBACK DE GOOGLE (esto es lo que te faltaba)
query_params = st.query_params
if 'code' in query_params and not st.session_state.user:
    code = query_params['code']
    
    try:
        # Intercambiar código por token
        token_url = "https://oauth2.googleapis.com/token"
        token_data = {
            "code": code,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "redirect_uri": REDIRECT_URI,
            "grant_type": "authorization_code"
        }
        
        token_response = requests.post(token_url, data=token_data)
        token_json = token_response.json()
        
        if "access_token" in token_json:
            # Obtener información del usuario
            userinfo_url = "https://www.googleapis.com/oauth2/v2/userinfo"
            headers = {"Authorization": f"Bearer {token_json['access_token']}"}
            userinfo_response = requests.get(userinfo_url, headers=headers)
            user_info = userinfo_response.json()
            
            email = user_info.get("email")
            name = user_info.get("name", email.split("@")[0])
            
            # Guardar o actualizar usuario en Firestore
            user_doc = db.collection("USUARIOS").document(email.upper())
            if not user_doc.get().exists:
                user_doc.set({
                    "USERNAME": email.upper(),
                    "NAMES": name,
                    "EMAIL": email,
                    "AUTH_METHOD": "google"
                })
            
            # Cargar datos del usuario
            st.session_state.user = user_doc.get().to_dict()
            
            # Limpiar parámetros de la URL
            st.query_params.clear()
            st.rerun()
            
    except Exception as e:
        st.error(f"Error en autenticación de Google: {e}")
        st.query_params.clear()

# 5. Interfaz de Login
if not st.session_state.user:
    st.title("🚀 ZTCHY PRO - Acceso")
    
    # URL de autenticación de Google
    auth_params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "scope": "openid email profile",
        "redirect_uri": REDIRECT_URI,
        "prompt": "select_account"
    }
    auth_url = f"https://accounts.google.com/o/oauth2/v2/auth?{urlencode(auth_params)}"
    
    # Botón de Google
    st.markdown(f"""
        <a href="{auth_url}" target="_self" style="
            text-decoration: none; display: block; text-align: center;
            padding: 12px; background-color: #4285F4; color: white;
            border-radius: 8px; font-weight: bold; margin: 20px 0;
        ">🔐 Entrar con Google</a>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # Acceso manual
    st.subheader("O ingresa manualmente")
    user_input = st.text_input("Usuario").upper()
    pass_input = st.text_input("Contraseña", type="password")
    
    if st.button("Ingresar", use_container_width=True):
        if user_input and pass_input:
            doc = db.collection("USUARIOS").document(user_input).get()
            if doc.exists and doc.to_dict().get("PASSWORD") == pass_input:
                st.session_state.user = doc.to_dict()
                st.rerun()
            else:
                st.error("❌ Usuario o contraseña no válidos.")
        else:
            st.warning("⚠️ Completa todos los campos")

# 6. Panel Principal
else:
    u = st.session_state.user
    st.sidebar.title(f"👤 {u.get('NAMES', 'Usuario')}")
    st.sidebar.write(f"**Email:** {u.get('EMAIL', 'N/A')}")
    
    if st.sidebar.button("🚪 Cerrar Sesión"):
        st.session_state.user = None
        st.rerun()
    
    st.header("🔎 Panel Seeker v6")
    st.success(f"✅ Sesión iniciada como: **{u.get('NAMES', 'Sin Nombre')}**")
    
    # Aquí va el resto de tu aplicación
    st.info("🎯 Aquí puedes agregar las funcionalidades de tu app")
