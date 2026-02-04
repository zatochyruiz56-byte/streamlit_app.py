import streamlit as st
from supabase import create_client

# 1. Conexión segura usando los Secrets de Streamlit
# Esto lee los datos de la "caja fuerte" que configuraste
try:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase = create_client(url, key)
except Exception as e:
    st.error("Error al leer los Secrets. Verifica la configuración en Streamlit Cloud.")
    st.stop()

st.set_page_config(page_title="ZTCHY-PRO", page_icon="🔥")

st.title("🔥 Bienvenido a ZTCHY-PRO")

# Control de navegación entre Registro y Verificación
if "esperando_otp" not in st.session_state:
    st.session_state.esperando_otp = False

# --- PANTALLA 1: REGISTRO ---
if not st.session_state.esperando_otp:
    st.subheader("Crear una nueva cuenta")
    
    with st.form("registro_form"):
        nuevo_user = st.text_input("Nombre de Usuario", placeholder="Ej: Luisluis")
        nuevo_email = st.text_input("Correo Electrónico")
        nueva_pass = st.text_input("Contraseña", type="password")
        btn_registro = st.form_submit_button("Registrarse")

        if btn_registro:
            if nuevo_user and nuevo_email and nueva_pass:
                try:
                    # Registrar usuario en el sistema de autenticación
                    res = supabase.auth.sign_up({"email": nuevo_email, "password": nueva_pass})
                    
                    # Insertar datos en la tabla 'perfiles' que creamos en el SQL Editor
                    # El saldo empezará en 0.00 automáticamente
                    supabase.table("perfiles").insert({
                        "id": res.user.id,
                        "username": nuevo_user,
                        "email": nuevo_email
                    }).execute()
                    
                    st.session_state.email_confirmar = nuevo_email
                    st.session_state.esperando_otp = True
                    st.success("¡Código enviado! Por favor, revisa tu correo.")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                st.warning("Por favor, completa todos los campos.")

# --- PANTALLA 2: VERIFICACIÓN ---
else:
    st.subheader("Verificación de Correo")
    st.info(f"Introduce el código de 8 dígitos enviado a: **{st.session_state.email_confirmar}**")
    
    codigo_input = st.text_input("Código OTP", placeholder="00000000")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Verificar Cuenta"):
            try:
                # Verificar el código en Supabase
                supabase.auth.verify_otp({
                    "email": st.session_state.email_confirmar,
                    "token": codigo_input,
                    "type": 'signup'
                })
                st.success("✅ ¡Cuenta activada! Ya puedes usar el servicio.")
                # Aquí podrías redirigir al Login o mostrar el saldo
                st.session_state.esperando_otp = False
            except:
                st.error("Código incorrecto o expirado. Inténtalo de nuevo.")
                
    with col2:
        if st.button("Volver al registro"):
            st.session_state.esperando_otp = False
            st.rerun()

# Pie de página simple
st.markdown("---")
st.caption("ZTCHY-PRO v2.0 - Sistema de Registro Seguro")
