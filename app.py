import streamlit as st
from supabase import create_client

# 1. Configuración de página
st.set_page_config(page_title="ZTCHY-PRO", page_icon="🛡️", layout="centered")

# Conexión
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_SECRET_KEY"] 
supabase = create_client(url, key)

# --- DISEÑO ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), 
                    url('https://images.unsplash.com/photo-1526392060635-9d6019884377?q=80&w=2070');
        background-size: cover;
    }
    .auth-card {
        background-color: white;
        padding: 40px;
        border-radius: 15px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.4);
    }
    .stButton > button {
        width: 100%;
        background: linear-gradient(90deg, #6c5ce7, #8e44ad);
        color: white;
        height: 3em;
        font-weight: bold;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

# Inicializar estados si no existen
if "view" not in st.session_state:
    st.session_state.view = "login"
if "email_temp" not in st.session_state:
    st.session_state.email_temp = ""

with st.container():
    st.markdown('<div class="auth-card">', unsafe_allow_html=True)
    
    # --- VISTA: LOGIN ---
    if st.session_state.view == "login":
        st.markdown("<h2 style='text-align:center; color:#333;'>Iniciar Sesión</h2>", unsafe_allow_html=True)
        email_in = st.text_input("Correo electrónico")
        pass_in = st.text_input("Contraseña", type="password")
        
        if st.button("Ingresar"):
            try:
                supabase.auth.sign_in_with_password({"email": email_in, "password": pass_in})
                st.success("¡Bienvenido!")
                st.balloons()
            except: st.error("Credenciales incorrectas")
        
        if st.button("👤 ¿No tienes cuenta? Regístrate"):
            st.session_state.view = "register"
            st.rerun()

    # --- VISTA: REGISTRO ---
    elif st.session_state.view == "register":
        st.markdown("<h2 style='text-align:center; color:#333;'>Crear Cuenta</h2>", unsafe_allow_html=True)
        u_name = st.text_input("Nombre de Usuario")
        u_email = st.text_input("Correo electrónico")
        u_pass = st.text_input("Contraseña", type="password")
        u_conf = st.text_input("Repetir Contraseña", type="password")
        
        if st.button("Completar Registro"):
            if u_pass != u_conf:
                st.error("Las contraseñas no coinciden")
            elif not u_name or not u_email:
                st.warning("Completa todos los campos")
            else:
                try:
                    # 1. Registro en Auth
                    res = supabase.auth.sign_up({"email": u_email, "password": u_pass})
                    # 2. Guardar en perfiles
                    if res.user:
                        supabase.table("perfiles").insert({
                            "id": res.user.id,
                            "username": u_name,
                            "email": u_email,
                            "saldo": 0.00
                        }).execute()
                        
                        # GUARDAR CORREO Y CAMBIAR VISTA
                        st.session_state.email_temp = u_email
                        st.session_state.view = "verify"
                        st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")
        
        if st.button("⬅️ Volver al Login"):
            st.session_state.view = "login"
            st.rerun()

    # --- VISTA: VERIFICACIÓN (AQUÍ PONDRÁS EL CÓDIGO) ---
    elif st.session_state.view == "verify":
        st.markdown("<h2 style='text-align:center; color:#333;'>Verificar Código</h2>", unsafe_allow_html=True)
        st.write(f"Introduce el código de 6 dígitos enviado a: **{st.session_state.email_temp}**")
        
        otp_code = st.text_input("Código de Verificación", placeholder="Ej: 067002")
        
        if st.button("Confirmar y Activar"):
            try:
                # Verificar el código en Supabase
                supabase.auth.verify_otp({
                    "email": st.session_state.email_temp,
                    "token": otp_code,
                    "type": 'signup'
                })
                st.success("✅ ¡Cuenta activada con éxito!")
                st.session_state.view = "login"
                # Esperar un poco para que el usuario vea el éxito
                st.rerun()
            except Exception as e:
                st.error("❌ Código incorrecto o expirado.")

        if st.button("Reintentar Registro"):
            st.session_state.view = "register"
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
