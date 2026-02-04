import streamlit as st
from supabase import create_client

# Conexión usando la Secret Key (para tener permisos de edición)
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_SECRET_KEY"]
supabase = create_client(url, key)

st.title("🛡️ Panel de Administración")
st.subheader("Recarga de Créditos ZTCHY-PRO")

# Protección por contraseña (la que pusiste en Secrets)
password_input = st.text_input("Introduce la clave de administrador", type="password")

if password_input == st.secrets["admin"]["password"]:
    st.success("Acceso autorizado")
    
    email_busqueda = st.text_input("Correo electrónico del cliente a recargar")
    
    if email_busqueda:
        # 1. Buscar al usuario en la tabla 'perfiles'
        res = supabase.table("perfiles").select("*").eq("email", email_busqueda).execute()
        
        if res.data:
            usuario = res.data[0]
            st.write(f"**Usuario encontrado:** {usuario['username']}")
            st.write(f"**Saldo actual:** ${usuario['saldo']}")
            
            monto = st.number_input("Cantidad a sumar ($)", min_value=0.0, step=10.0)
            
            if st.button("Confirmar Recarga"):
                nuevo_saldo = float(usuario['saldo']) + monto
                # 2. Actualizar el saldo en la base de datos
                supabase.table("perfiles").update({"saldo": nuevo_saldo}).eq("email", email_busqueda).execute()
                
                st.balloons()
                st.success(f"¡Recarga exitosa! Nuevo saldo: ${nuevo_saldo}")
        else:
            st.error("No se encontró ningún usuario con ese correo.")
else:
    if password_input:
        st.error("Contraseña incorrecta")
