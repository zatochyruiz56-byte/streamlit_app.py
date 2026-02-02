import streamlit as st
import requests

# Configuración de la página
st.set_page_config(page_title="DataAPI Premium", page_icon="💳")
st.title("💳 Consulta DNI Premium")

# --- TUS CREDENCIALES ---
API_URL = "https://seeker-v6.com/api/v1/personas/apiPremium/dni"
TOKEN = "sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"

# Interfaz de usuario
dni = st.text_input("Ingresa el DNI a consultar:", max_chars=8)

if st.button("Consultar Ahora"):
    if len(dni) == 8:
        # 1. Ajuste de Headers (Imagen 19)
        headers = {
            "Authorization": f"Bearer {TOKEN}"
        }
        
        # 2. Ajuste de Payload (Imagen 1 y 19)
        # Usamos 'data' para enviar como application/x-www-form-urlencoded
        payload = {"dni": dni}
        
        try:
            with st.spinner("Conectando con DataAPI..."):
                # Realizamos la petición POST
                response = requests.post(API_URL, headers=headers, data=payload)
                
                # Verificamos si la respuesta es válida
                if response.status_code == 200:
                    data = response.json()
                    
                    if data.get("status") == "success":
                        st.success("✅ Información obtenida correctamente")
                        
                        # Mostramos los datos de forma limpia
                        datos_persona = data.get("data", {})
                        st.write("### Resultados:")
                        st.json(datos_persona)
                        
                        # Mostramos créditos restantes
                        st.metric("Créditos Restantes", data.get("creditos_restantes"))
                    else:
                        st.error(f"Error de la API: {data.get('message')}")
                
                elif response.status_code == 401:
                    st.error("❌ Token inválido o expirado. Revisa tu panel de DataAPI.")
                else:
                    st.error(f"Error del servidor (Código {response.status_code})")
                    st.info("Detalle técnico: La API no respondió un formato conocido.")
                    
        except Exception as e:
            st.error(f"Error crítico de conexión: {e}")
    else:
        st.warning("⚠️ El DNI debe tener exactamente 8 números.")

st.divider()
st.caption("Conexión segura establecida mediante servidor - Sin bloqueos de CORS")
