import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="SEEKER v6", page_icon="🔍", layout="centered")

# --- 2. ESTILO VISUAL (Personalización SEEKER) ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #4facfe 0%, #00f2fe 50%, #f093fb 100%); }
    .main-card { 
        background: white; 
        padding: 30px; 
        border-radius: 20px; 
        box-shadow: 0 10px 30px rgba(0,0,0,0.2); 
        color: #333;
    }
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; }
    </style>
""", unsafe_allow_html=True)

# --- 3. CONEXIÓN FIREBASE (Con limpieza de llave PEM) ---
if not firebase_admin._apps:
    try:
        # Extraemos los datos del bloque [firebase] en Secrets
        fb_creds = dict(st.secrets["firebase"])
        # Limpiamos los saltos de línea para evitar el error 'Unable to load PEM file'
        fb_creds["private_key"] = fb_creds["private_key"].replace("\\n", "\n")
        
        cred = credentials.Certificate(fb_creds)
        firebase_admin.initialize_app(cred)
    except Exception as e:
        st.error(f"Error crítico de conexión: {e}")
        st.stop()

db = firestore.client()

# --- 4. LÓGICA DE NAVEGACIÓN ---
if 'user' not in st.session_state:
    st.session_state.user = None

# --- VISTA: LOGIN ---
if not st.session_state.user:
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.title("SEEKER v6")
    st.subheader("Iniciar Sesión")

    # Botón Google (Usa el redirect_uri configurado en Google Cloud)
    client_id = st.secrets["google_client_id"]
    # Esta URL debe ser idéntica a la registrada en la Consola de Google
    redirect_uri = "https://appappppy-43nnqkr6ctadmkdomd2nxc.streamlit.app/"
    google_auth_url = (
        f"https://accounts.google.com/o/oauth2/v2/auth?"
        f"client_id={client_id}&"
        f"response_type=code&"
        f"scope=openid%20email%20profile&"
        f"redirect_uri={redirect_uri}"
    )
    
    st.link_button("🌐 Ingresar con Google", google_auth_url)
    
    st.write("--- o usa tu cuenta local ---")
    
    # Login Manual para usuario ZATOCHY
    u_input = st.text_input("Nombre de Usuario").upper()
    p_input = st.text_input("Contraseña", type="password")

    if st.button("Ingresar"):
        if u_input:
            doc_ref = db.collection("COLECCION").document(u_input).get()
            if doc_ref.exists:
                user_data = doc_ref.to_dict()
                if user_data.get("PASSWORD") == p_input:
                    st.session_state.user = user_data
                    st.rerun()
                else:
                    st.error("Contraseña incorrecta.")
            else:
                st.error("El usuario no existe en la base de datos.")
        else:
            st.warning("Por favor, ingresa un nombre de usuario.")

    st.markdown('</div>', unsafe_allow_html=True)

# --- VISTA: PANEL PRINCIPAL (SEEKER LOGUEADO) ---
else:
    user = st.session_state.user
    # Barra lateral con datos de Firebase
    st.sidebar.title(f"Hola, {user.get('USERNAME', 'Usuario')}")
    st.sidebar.metric("Tus Créditos", f"S/ {user.get('creditos', 0)}")
    st.sidebar.write(f"Estado: **{user.get('estado', 'N/A')}**")
    
    if st.sidebar.button("Cerrar Sesión"):
        st.session_state.user = None
        st.rerun()

    # Contenido de la Aplicación
    st.title("🔎 Panel de Consultas")
    st.write(f"Bienvenido de nuevo, **{user.get('NAMES', 'Usuario')}**.")
    
    # Ejemplo de Menú de Herramientas
    opcion = st.selectbox("¿Qué deseas consultar hoy?", [
        "Seleccione...", "Consulta Placa", "DNI Virtual", "Búsqueda Nombres", "Ficha Reniec"
    ])
    
    if opcion != "Seleccione...":
        st.info(f"Has seleccionado: {opcion}. (Aquí programaremos la lógica de búsqueda).")
