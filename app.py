import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import requests

# --- 1. INICIALIZACIÓN DE ESTADO ---
if 'user' not in st.session_state:
    st.session_state.user = None

# --- 2. CONEXIÓN FIREBASE ---
if not firebase_admin._apps:
    try:
        fb_creds = dict(st.secrets["firebase"])
        fb_creds["private_key"] = fb_creds["private_key"].replace("\\n", "\n")
        cred = credentials.Certificate(fb_creds)
        firebase_admin.initialize_app(cred)
    except Exception as e:
        st.error(f"Error Firebase: {e}")

db = firestore.client()

# --- 3. LÓGICA DE RETORNO (Captura el login de Google) ---
# Si Google nos envía de vuelta con un 'code' en la URL
query_params = st.query_params
if "code" in query_params and not st.session_state.user:
    # Aquí es donde SEEKER procesa el retorno automáticamente
    # Por ahora, simularemos el éxito para que entres directo
    st.session_state.user = {"USERNAME": "ZATOCHY", "NAMES": "Usuario Google", "creditos": 0}
    st.rerun()

# --- 4. DISEÑO VISUAL ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #00c6ff, #0072ff); }
    .login-card { background: white; padding: 2.5rem; border-radius: 20px; box-shadow: 0 15px 35px rgba(0,0,0,0.3); color: #333; text-align: center; }
    </style>
""", unsafe_allow_html=True)

# --- VISTA: LOGIN ---
if not st.session_state.user:
    st.markdown('<div class="login-card">', unsafe_allow_html=True)
    st.title("ZATOCHY PRO")
    st.subheader("SEEKER v6")
    
    # DATOS DE GOOGLE
    client_id = st.secrets["google_client_id"]
    redirect_uri = "https://appappppy-43nnqkr6ctadmkdomd2nxc.streamlit.app/"
    auth_url = (
        f"https://accounts.google.com/o/oauth2/v2/auth?"
        f"client_id={client_id}&"
        f"response_type=code&"
        f"scope=openid%20email%20profile&"
        f"redirect_uri={redirect_uri}&"
        f"prompt=select_account"
    )

    # BOTÓN QUE ACTÚA EN LA MISMA PESTAÑA (_self)
    st.markdown(f"""
        <a href="{auth_url}" target="_self" style="
            text-decoration: none; display: block;
            padding: 15px; background-color: #4285F4; color: white;
            border-radius: 10px; font-weight: bold; font-size: 1.1em;
            box-shadow: 0 4px 15px rgba(66,133,244,0.3);
        ">🌐 Ingresar con Google</a>
    """, unsafe_allow_html=True)

    st.write("--- o accede manualmente ---")
    u_in = st.text_input("Usuario").upper()
    p_in = st.text_input("Contraseña", type="password")
    
    if st.button("Ingresar al Sistema", use_container_width=True):
        doc = db.collection("COLECCION").document(u_in).get()
        if doc.exists and doc.to_dict().get("PASSWORD") == p_in:
            st.session_state.user = doc.to_dict()
            st.rerun()
        else:
            st.error("Acceso denegado.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- VISTA: PANEL PRINCIPAL ---
else:
    user = st.session_state.user
    st.sidebar.title(f"Bienvenido, {user.get('USERNAME')}")
    st.sidebar.metric("Créditos", f"S/ {user.get('creditos', 0)}")
    
    if st.sidebar.button("Log Out"):
        st.session_state.user = None
        st.query_params.clear()
        st.rerun()
    
    st.title("🔎 Panel de Búsqueda")
    st.info("Ya puedes realizar tus consultas en el menú lateral.")
