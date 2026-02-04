import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# --- 1. INICIALIZACIÓN DE ESTADO (Evita AttributeError) ---
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

# --- 3. DISEÑO SEEKER ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #4facfe, #f093fb); }
    .login-card { background: white; padding: 2rem; border-radius: 15px; box-shadow: 0 10px 25px rgba(0,0,0,0.2); color: #333; }
    </style>
""", unsafe_allow_html=True)

# --- VISTA: LOGIN ---
if not st.session_state.user:
    st.markdown('<div class="login-card">', unsafe_allow_html=True)
    st.title("Iniciar Sesión - SEEKER v6")
    
    # LÓGICA DE GOOGLE
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

    # BOTÓN HTML QUE ABRE EN LA MISMA PESTAÑA (_self)
    st.markdown(f"""
        <a href="{auth_url}" target="_self" style="
            text-decoration: none; display: block; text-align: center;
            padding: 12px; background-color: #4285F4; color: white;
            border-radius: 8px; font-weight: bold; margin-bottom: 20px;
        ">🌐 Ingresar con Google</a>
    """, unsafe_allow_html=True)

    st.write("---")
    user_in = st.text_input("Usuario (Ej: ZATOCHY)").upper()
    pass_in = st.text_input("Contraseña", type="password")
    
    if st.button("Ingresar", use_container_width=True):
        doc = db.collection("COLECCION").document(user_in).get()
        if doc.exists and doc.to_dict().get("PASSWORD") == pass_in:
            st.session_state.user = doc.to_dict()
            st.rerun()
        else:
            st.error("Credenciales incorrectas.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- VISTA: PANEL PRINCIPAL ---
else:
    user = st.session_state.user
    st.sidebar.title(f"Hola, {user['USERNAME']}")
    st.sidebar.metric("Créditos", f"S/ {user['creditos']}")
    
    if st.sidebar.button("Cerrar Sesión"):
        st.session_state.user = None
        st.rerun()
    
    st.title("🔎 Panel de Consultas")
    st.write(f"Bienvenido, {user['NAMES']}.")
