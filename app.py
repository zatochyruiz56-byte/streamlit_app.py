import streamlit as st
import requests

# Configuración de la página
st.set_page_config(page_title="DataAPI Premium", page_icon="💳")
st.title("💳 Consulta DNI Premium")

# --- CREDENCIALES CORREGIDAS SEGÚN IMAGEN 19/20 ---
# Nota: Se eliminó /api/v1/ porque la documentación muestra la ruta directa
API_URL = "https://seeker-v6.com/personas/apiPremium/dni"
TOKEN = "sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"

dni = st.text_input("Ingresa el DNI a consultar:", max_chars=8)

if st.button("Consultar Ahora"):
    if len(dni) == 8:
        # Headers según Imagen 19
        headers = {
            "Authorization": f"Bearer {TOKEN}"
        }
        
        # Datos según Imagen 20 (Formato data=)
        payload = {"dni": dni}
        
        try:
            with st.spinner("Buscando información..."):
                # Realizamos la petición
                response = requests.post(API_URL, headers=headers, data=payload)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if data.get("status") == "success":
                        st.success("✅ Datos encontrados")
                        st.json(data.get("data"))
                        st.metric("Créditos Restantes", data.get("creditos_restantes"))
                    else:
                        st.error(f"Error de la API: {data.get('message')}")
                
                elif response.status_code == 404:
                    st.error("❌ Error 404: La URL de la API es incorrecta. Verifica si falta o sobra '/api/v1/'")
                else:
                    st.error(f"Error {response.status_code}: {response.text}")
                    
        except Exception as e:
            st.error(f"Error de conexión: {e}")
    else:
        st.warning("⚠️ Ingresa un DNI de 8 dígitos.")

st.divider()
st.caption("Conexión segura vía servidor - Sin errores de CORS")
