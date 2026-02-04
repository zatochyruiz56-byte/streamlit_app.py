import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# --- 1. CONFIGURACIÓN INICIAL (EVITA ATTRIBUTEERROR) ---
st.set_page_config(page_title="ZTCHY PRO", page_icon="🔍")

if 'user' not in st.session_state:
    st.session_state.user = None

# --- 2. CONEXIÓN FIREBASE (RESISTENTE A ERRORES) ---
if not firebase_admin._apps:
    try:
        # Extraemos los datos de Secrets
        fb_creds = dict(st.secrets["firebase"])
        # Limpieza de la llave PEM para evitar errores de carga
        fb_creds["private_key"] = fb_creds["private_key"].replace("\\n", "\n").strip()
        
        cred = credentials.Certificate(fb_creds)
        firebase_admin.initialize_app(cred)
    except Exception as e:
        st.error(f"Error en la configuración de Firebase: {e}")
        st.info("Revisa que los Secrets estén bien pegados.")
        st.stop()

db = firestore.client()

# --- 3. ESTILO VISUAL ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #00c6ff, #0072ff); }
    .login-card { 
        background: white; padding: 2rem; border-radius: 15px; 
        box-shadow: 0 10px 25px rgba(0,0,0,0.2); color: #333; 
    }
    </style>
""", unsafe_allow_html=True)

# --- 4. LÓGICA DE LOGIN ---
if not st.session_state.user:
    st.markdown('<div class="login-card">', unsafe_allow_html=True)
    st.title("🚀 ZTCHY PRO")
    st.subheader("SEEKER v6")

    # Configuración de Google
    client_id = st.secrets["google_client_id"]
    # IMPORTANTE: Este link debe ser igual al de tu consola de Google
    redirect_uri = "https://appappppy-43nnqkr6ctadmkdomd2nxc.streamlit.app/"
    
    auth_url = (
        f"https://accounts.google.com/o/oauth2/v2/auth?"
        f"client_id={client_id}&"
        f"response_type=code&"
        f"scope=openid%20email%20profile&"
        f"redirect_uri={redirect_uri}&"
        f"prompt=select_account"
    )

    # BOTÓN HTML PARA CARGAR EN LA MISMA PESTAÑA (_self)
    st.markdown(f"""
        <a href="{auth_url}" target="_self" style="
            text-decoration: none; display: block; text-align: center;
            padding: 15px; background-color: #4285F4; color: white;
            border-radius: 10px; font-weight: bold; margin-bottom: 20px;
        ">🌐 Ingresar con Google</a>
    """, unsafe_allow_html=True)

    st.write("--- o usa acceso manual ---")
    u_in = st.text_input("Usuario").upper()
    p_in = st.text_input("Contraseña", type="password")
    
    if st.button("Acceder", use_container_width=True):
        doc = db.collection("COLECCION").document(u_in).get()
        if doc.exists and doc.to_dict().get("PASSWORD") == p_in:
            st.session_state.user = doc.to_dict()
            st.rerun()
        else:
            st.error("Credenciales incorrectas.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- 5. PANEL PRINCIPAL ---
else:
    user = st.session_state.user
    st.sidebar.title(f"Hola, {user.get('USERNAME', 'ZATOCHY')}")
    st.sidebar.metric("Créditos", f"S/ {user.get('creditos', 0)}")
    
    if st.sidebar.button("Cerrar Sesión"):
        st.session_state.user = None
        st.rerun()

    st.title("🔎 Panel de Búsquedas")
    st.success(f"Conectado como: {user.get('NAMES')}")
    st.write("Selecciona una herramienta en el menú lateral.")
