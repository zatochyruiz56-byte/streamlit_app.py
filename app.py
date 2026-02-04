import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# --- 1. CONFIGURACIÓN E INYECCIÓN DE INTERFAZ (EL MURO) ---
st.set_page_config(page_title="ZTCHY PRO", layout="centered", initial_sidebar_state="collapsed")

# Muro visual de Machu Picchu
st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), 
                    url("https://images.unsplash.com/photo-1526392060635-9d6019884377?q=80&w=2070&auto=format&fit=crop");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    /* Bloqueo total del Sidebar si no está autenticado */
    [data-testid="stSidebar"] {{
        display: {"block" if st.session_state.get('auth_active', False) else "none"};
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. INICIALIZACIÓN ÚNICA DE FIREBASE ---
if not firebase_admin._apps:
    fb_dict = dict(st.secrets["firebase"])
    fb_dict["private_key"] = fb_dict["private_key"].replace('\\n', '\n')
    cred = credentials.Certificate(fb_dict)
    firebase_admin.initialize_app(cred)

db = firestore.client()

# --- 3. CONTROLADOR DE FLUJO (LA LÓGICA CEREBRO) ---
# Inicializamos el estado si no existe
if "auth_active" not in st.session_state:
    st.session_state.auth_active = False
if "user_session" not in st.session_state:
    st.session_state.user_session = None

# Función para cerrar sesión desde cualquier lugar
def logout():
    st.session_state.auth_active = False
    st.session_state.user_session = None
    st.rerun()

# --- 4. EL FILTRO DE SEGURIDAD ---
if not st.session_state.auth_active:
    # CAPA 1: Solo Login y Registro
    # Aquí puedes importar tus funciones de login o ponerlas directo
    import login_module # O el nombre que le des a tu archivo de login
    login_module.show_auth_page()
else:
    # CAPA 2: La Aplicación Real (Consultas y Saldo)
    # Esta parte es invisible e inalcanzable sin auth_active = True
    import main_panel # Tu archivo con la lógica de consultas
    main_panel.show_dashboard(db, logout)
