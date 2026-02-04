import streamlit as st
from supabase import create_client

# Configuración de conexión
URL_SUPABASE = "https://xbyvblijoieqhczldmar.supabase.co"
# Usamos la Publishable Key para la app del cliente
KEY_SUPABASE = "sb_publishable_JIOygyvamZAsV0WALqlenw_lEeZjXJa"
supabase = create_client(URL_SUPABASE, KEY_SUPABASE)

st.set_page_config(page_title="ZTCHY-PRO Registro", page_icon="🚀")

st.title("🚀 Registro de Usuario")

# Control de estados de la pantalla
if "paso_verificacion" not in st.session_state:
    st.session_state.paso_verificacion = False

if not st.session_state.paso_verificacion:
    with st.form("form_registro"):
        u_name = st.text_input("Nombre de Usuario")
        u_email = st.text_input("Correo Electrónico")
        u_pass = st.text_input("Contraseña", type="password")
        btn_reg = st.form_submit_button("Crear Cuenta")

        if btn_reg:
            try:
                # 1. Registrar en el sistema de autenticación
                res = supabase.auth.sign_up({"email": u_email, "password": u_pass})
                
                # 2. Crear el perfil en nuestra tabla de saldos
                # Nota: El saldo inicia en 0.00 por defecto
                supabase.table("perfiles").insert({
                    "id": res.user.id,
                    "username": u_name,
                    "email": u_email
                }).execute()
                
                st.session_state.email_temporal = u_email
                st.session_state.paso_verificacion = True
                st.success("¡Código enviado! Revisa tu correo.")
                st.rerun()
            except Exception as e:
                st.error(f"Error al registrar: {e}")
else:
    # --- Pantalla para introducir el código OTP ---
    st.info(f"Ingresa el código enviado a: {st.session_state.email_temporal}")
    codigo = st.text_input("Código de Verificación", help="Revisa tu carpeta de spam si no lo ves")
    
    if st.button("Verificar y Activar"):
        try:
            supabase.auth.verify_otp({
                "email": st.session_state.email_temporal,
                "token": codigo,
                "type": 'signup'
            })
            st.success("✅ ¡Cuenta activada con éxito! Ya puedes iniciar sesión.")
            if st.button("Ir al Login"):
                st.session_state.paso_verificacion = False
                st.rerun()
        except:
            st.error("Código inválido. Inténtalo de nuevo.")
