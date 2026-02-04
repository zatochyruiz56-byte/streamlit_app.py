import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth

# CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="ZTCHY-PRO", page_icon="🛡️")

# ESTILO VISUAL (Fondo Machu Picchu + Tarjeta Blanca)
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), 
                    url('https://images.unsplash.com/photo-1526392060635-9d6019884377?q=80&w=2070');
        background-size: cover;
    }
    .auth-card {
        background-color: white !important;
        padding: 40px;
        border-radius: 15px;
        color: black !important;
        max-width: 500px;
        margin: auto;
    }
    h2, label, p { color: black !important; font-weight: bold !important; }
    .stButton>button { background-color: #6c5ce7 !important; color: white !important; width: 100%; border: none; height: 45px; }
    </style>
    """, unsafe_allow_html=True)

# INICIALIZACIÓN DE FIREBASE
if not firebase_admin._apps:
    try:
        # Extraemos la clave privada manejando correctamente los saltos de línea \n
        private_key = st.secrets["firebase"]["private_key"].replace('\\n', '\n')
        
        fb_credentials = {
            "type": st.secrets["firebase"]["type"],
            "project_id": st.secrets["firebase"]["project_id"],
            "private_key_id": st.secrets["firebase"]["private_key_id"],
            "private_key": private_key,
            "client_email": st.secrets["firebase"]["client_email"],
            "client_id": st.secrets["firebase"]["client_id"],
            "auth_uri": st.secrets["firebase"]["auth_uri"],
            "token_uri": st.secrets["firebase"]["token_uri"],
            "auth_provider_x509_cert_url": st.secrets["firebase"]["auth_provider_x509_cert_url"],
            "client_x509_cert_url": st.secrets["firebase"]["client_x509_cert_url"]
        }
        cred = credentials.Certificate(fb_credentials)
        firebase_admin.initialize_app(cred)
    except Exception as e:
        st.error(f"Error de configuración: {e}")

# LÓGICA DE NAVEGACIÓN
if "view" not in st.session_state: st.session_state.view = "login"

st.markdown('<div class="auth-card">', unsafe_allow_html=True)

if st.session_state.view == "login":
    st.markdown("<h2>Iniciar Sesión</h2>", unsafe_allow_html=True)
    user_email = st.text_input("Correo Electrónico")
    user_pass = st.text_input("Contraseña", type="password")
    
    if st.button("INGRESAR"):
        try:
            # Verificamos si el usuario existe en Firebase
            user = auth.get_user_by_email(user_email)
            st.success(f"¡Bienvenido, {user.email}!")
            st.balloons()
        except:
            st.error("Credenciales inválidas o usuario no registrado.")
            
    if st.button("¿No tienes cuenta? Regístrate aquí"):
        st.session_state.view = "register"
        st.rerun()

elif st.session_state.view == "register":
    st.markdown("<h2>Crear Nueva Cuenta</h2>", unsafe_allow_html=True)
    reg_email = st.text_input("Tu mejor Email")
    reg_pass = st.text_input("Contraseña (mínimo 6 caracteres)", type="password")
    
    if st.button("REGISTRARME"):
        if len(reg_pass) < 6:
            st.warning("La contraseña debe tener al menos 6 caracteres.")
        else:
            try:
                user = auth.create_user(email=reg_email, password=reg_pass)
                st.success("✅ ¡Cuenta creada exitosamente!")
                st.info("Ahora puedes volver para iniciar sesión.")
            except Exception as e:
                st.error(f"Error en el registro: {e}")
                
    if st.button("Volver al Login"):
        st.session_state.view = "login"
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)
