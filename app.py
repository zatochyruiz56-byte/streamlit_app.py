import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# --- 1. INICIALIZACIÓN DE ESTADO ---
if 'user' not in st.session_state:
    st.session_state.user = None

# --- 2. CONEXIÓN FIREBASE (Limpieza de llave PEM) ---
if not firebase_admin._apps:
    try:
        fb_creds = dict(st.secrets["firebase"])
        # Esta línea es vital para corregir el error "Unable to load PEM file"
        fb_creds["private_key"] = fb_creds["private_key"].replace("\\n", "\n")
        cred = credentials.Certificate(fb_creds)
        firebase_admin.initialize_app(cred)
    except Exception as e:
        st.error(f"Error de conexión Firebase: {e}")

db = firestore.client()

# --- 3. LÓGICA DE DETECCIÓN DE LOGIN (RETORNO) ---
# Si regresas de Google con un código, te logueamos automáticamente
if "code" in st.query_params and not st.session_state.user:
    st.session_state.user = {"USERNAME": "ZATOCHY", "NAMES": "Zatochy Ruiz", "creditos": 0}
    st.rerun()

# --- 4. INTERFAZ SEEKER ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #00c6ff 0%, #0072ff 100%); }
    .login-box { background: white; padding: 30px; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.3); color: #333; text-align: center; }
    </style>
""", unsafe_allow_html=True)

if not st.session_state.user:
    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    st.title("🚀 ZTCHY PRO")
    st.subheader("SEEKER v6")
    
    # URL de Google con redirect_uri exacto
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

    # BOTÓN HTML PARA CARGAR EN LA MISMA PESTAÑA
    st.markdown(f"""
        <a href="{auth_url}" target="_self" style="
            text-decoration: none; display: block; padding: 12px;
            background-color: #4285F4; color: white; border-radius: 10px;
            font-weight: bold; margin-bottom: 15px;
        ">🌐 Ingresar con Google</a>
    """, unsafe_allow_html=True)

    st.write("--- o usa tu cuenta local ---")
    u_in = st.text_input("Usuario").upper()
    p_in = st.text_input("Contraseña", type="password")
    
    if st.button("Ingresar", use_container_width=True):
        doc = db.collection("COLECCION").document(u_in).get()
        if doc.exists and doc.to_dict().get("PASSWORD") == p_in:
            st.session_state.user = doc.to_dict()
            st.rerun()
        else:
            st.error("Credenciales incorrectas.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- PANEL PRINCIPAL (ZATOCHY LOGUEADO) ---
else:
    user = st.session_state.user
    st.sidebar.title(f"Hola, {user.get('USERNAME', 'ZATOCHY')}")
    st.sidebar.metric("Créditos", f"S/ {user.get('creditos', 0)}")
    
    if st.sidebar.button("Salir"):
        st.session_state.user = None
        st.query_params.clear()
        st.rerun()

    st.title("🔎 Panel de Consultas")
    st.success(f"Conectado como: {user.get('NAMES')}")
