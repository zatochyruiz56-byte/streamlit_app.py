import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# --- CONEXIÓN SEGURA A FIREBASE ---
def iniciar_db():
    if not firebase_admin._apps:
        try:
            # Trae los datos de la sección [firebase] de tus Secrets
            info = dict(st.secrets["firebase"])
            # Limpia la llave para evitar el error de "InvalidByte"
            info["private_key"] = info["private_key"].replace("\\n", "\n")
            
            cred = credentials.Certificate(info)
            firebase_admin.initialize_app(cred)
        except Exception as e:
            st.error(f"Error en la llave de Firebase: {e}")
            st.stop()
    return firestore.client()

db = iniciar_db()

# --- DISEÑO SEEKER V6 ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #4facfe, #f093fb); }
    .card { background: white; padding: 2rem; border-radius: 15px; color: #333; box-shadow: 0 10px 25px rgba(0,0,0,0.1); }
    </style>
""", unsafe_allow_html=True)

if 'user' not in st.session_state: st.session_state.user = None

# --- PANTALLA DE LOGIN ---
if not st.session_state.user:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.title("Iniciar Sesión - SEEKER v6")
    
    # Botón de Google Real
    g_id = st.secrets["google_client_id"]
    url_g = f"https://accounts.google.com/o/oauth2/v2/auth?client_id={g_id}&response_type=code&scope=openid%20email%20profile&redirect_uri=https://appappppy-43nnqkr6ctadmkdomd2nxc.streamlit.app/"
    
    st.link_button("🌐 Ingresar con Google", url_g)
    st.write("--- o entra manualmente ---")
    
    user_in = st.text_input("Nombre de Usuario (Ej: ZATOCHY)").upper()
    pass_in = st.text_input("Contraseña", type="password")
    
    if st.button("Ingresar"):
        # Busca en tu COLECCION -> ZATOCHY
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
    # --- PANEL PRINCIPAL TRAS LOGUEARSE ---
    st.sidebar.title(f"Hola, {st.session_state.user['USERNAME']}")
    st.sidebar.metric("Créditos", f"S/ {st.session_state.user['creditos']}") #
    
    st.write(f"## Bienvenido al buscador, {st.session_state.user['NAMES']}")
    
    if st.sidebar.button("Cerrar Sesión"):
        st.session_state.user = None
        st.rerun()
