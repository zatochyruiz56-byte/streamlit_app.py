import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# 1. INICIALIZACIÓN (Evita AttributeError en línea 5)
if 'user' not in st.session_state:
    st.session_state.user = None

# 2. FIREBASE CON MANEJO DE ERRORES
if not firebase_admin._apps:
    try:
        fb_creds = dict(st.secrets["firebase"])
        # Limpiamos posibles errores de formato en la llave
        fb_creds["private_key"] = fb_creds["private_key"].replace("\\n", "\n").strip()
        cred = credentials.Certificate(fb_creds)
        firebase_admin.initialize_app(cred)
    except Exception as e:
        st.error(f"Error crítico de llave: {e}")
        st.stop()

db = firestore.client()

# 3. INTERFAZ DE LOGIN
if not st.session_state.user:
    st.title("🚀 ZTCHY PRO")
    
    client_id = st.secrets["google_client_id"]
    # ESTE LINK DEBE SER IGUAL AL DE LA CONSOLA
    redirect_uri = "https://appappppy-43nnqkr6ctadmkdomd2nxc.streamlit.app/"
    
    auth_url = (
        f"https://accounts.google.com/o/oauth2/v2/auth?"
        f"client_id={client_id}&"
        f"response_type=code&"
        f"scope=openid%20email%20profile&"
        f"redirect_uri={redirect_uri}&"
        f"prompt=select_account"
    )

    # BOTÓN PARA MISMA PESTAÑA
    st.markdown(f"""
        <a href="{auth_url}" target="_self" style="
            text-decoration: none; display: block; text-align: center;
            padding: 15px; background-color: #4285F4; color: white;
            border-radius: 10px; font-weight: bold;
        ">🌐 Ingresar con Google</a>
    """, unsafe_allow_html=True)
    
    st.write("---")
    # ... (Aquí va tu login manual si lo necesitas)
    
else:
    st.write(f"Bienvenido, {st.session_state.user.get('NAMES')}")
    if st.button("Cerrar Sesión"):
        st.session_state.user = None
        st.rerun()
