import streamlit as st
from supabase import create_client

# 1. Conexión usando st.secrets (la "caja fuerte" de Streamlit)
# Esto evita que GitHub detecte tus llaves como públicas
try:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase = create_client(url, key)
except Exception as e:
    st.error("Error de configuración: Faltan los Secrets en Streamlit Cloud.")
    st.stop()

st.set_page_config(page_title="ZTCHY-PRO", page_icon="🚀")

# Estilos visuales simples
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #007bff; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 Registro de Usuario")

# Controlamos si estamos en paso de Registro o paso de Verificación
if "esperando_otp" not in st.session_state:
    st.session_state.esperando_otp = False

if not st.session_state.esperando_otp:
    # --- PANTALLA DE REGISTRO ---
    with st.container():
        user_name = st.text_input("Nombre de Usuario", placeholder="Ej: Luisluis")
        email = st.text_input("Correo Electrónico", placeholder="tu@email.com")
        password = st.text_input("Contraseña", type="password")
        
        if st.button("Crear Cuenta"):
            if user_name and email and password:
                try:
                    # Registrar en Supabase Auth (esto dispara el correo con el código)
                    auth_res = supabase.auth.sign_up({"email": email, "password": password})
                    
                    # Insertar el perfil en la tabla que creamos (con saldo 0)
                    supabase.table("perfiles").insert({
                        "id": auth_res.user.id,
                        "username": user_name,
                        "email": email
                    }).execute()
                    
                    st.session_state.email_temporal = email
                    st.session_state.esperando_otp = True
                    st.success("✅ ¡Código enviado! Revisa tu bandeja de entrada.")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error al registrar: {e}")
            else:
                st.warning("⚠️ Completa todos los campos antes de continuar.")

else:
    # --- PANTALLA DE VERIFICACIÓN (CÓDIGO OTP) ---
    st.subheader("Confirmar Correo")
    st.info(f"Ingresa el código que enviamos a: **{st.session_state.email_temporal}**")
    
    otp_code = st.text_input("Código de Verificación (8 dígitos)", placeholder="00000000")
    
    if st.button("Verificar y Activar Cuenta"):
        try:
            supabase.auth.verify_otp({
                "email": st.session_state.email_temporal,
                "token": otp_code,
                "type": 'signup'
            })
            st.success("🎉 ¡Cuenta verificada! Ya puedes usar la aplicación.")
            # Aquí podrías poner un botón para ir al login o mostrar el saldo inicial
            if st.button("Comenzar"):
                st.session_state.esperando_otp = False
                st.rerun()
        except Exception as e:
            st.error("❌ Código incorrecto o expirado. Inténtalo de nuevo.")

    if st.button("⬅️ Volver al inicio"):
        st.session_state.esperando_otp = False
        st.rerun()
