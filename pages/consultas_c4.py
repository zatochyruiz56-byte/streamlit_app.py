import streamlit as st
import requests

# --- CONFIGURACIÓN DEL TOKEN Y URL ---
# He configurado tu token personal sk_live directamente en las cabeceras
API_URL = "https://seeker-v6.com/personas/api/consultapremiunc4"
API_TOKEN = "sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"

def realizar_consulta_c4(dni):
    """
    Función para realizar la petición POST a la API de Seeker-V6
    """
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "dni": dni
    }
    
    try:
        # Se envía el DNI dentro del cuerpo JSON como pide la documentación
        response = requests.post(API_URL, headers=headers, json=payload, timeout=15)
        return response
    except Exception as e:
        return f"Error de conexión: {e}"

# --- INTERFAZ DE STREAMLIT ---
st.set_page_config(page_title="Consulta C4 - DataAPI", page_icon="👤")

st.title("👤 Consulta Premiun C4")
st.markdown("---")

st.write("Ingrese el DNI para obtener la información completa de RENIEC.")

# Entrada de texto limitada a 8 caracteres (DNI peruano)
dni = st.text_input("DNI (8 dígitos)", max_chars=8, placeholder="Ej: 12345678")

if st.button("Consultar Datos", use_container_width=True):
    if len(dni) == 8 and dni.isdigit():
        with st.spinner("Consultando base de datos de RENIEC..."):
            res = realizar_consulta_c4(dni)
            
            if isinstance(res, str):
                st.error(res)
            else:
                if res.status_code == 200:
                    data = res.json()
                    
                    if data.get("status") == "success":
                        st.success("✅ Datos recuperados exitosamente")
                        
                        # Mostrar créditos restantes en la barra lateral
                        if "creditos_restantes" in data:
                            st.sidebar.info(f"Saldo: {data['creditos_restantes']} créditos")
                        
                        # Mostrar el resultado JSON formateado
                        st.subheader("Resultados de la Consulta")
                        st.json(data)
                    else:
                        st.warning(f"La API respondió con un error: {data.get('message', 'Sin mensaje')}")
                        st.json(data)
                elif res.status_code == 401:
                    st.error("❌ Token inválido. Revisa tu suscripción en DataAPI.")
                elif res.status_code == 402:
                    st.error("❌ Saldo insuficiente.")
                else:
                    st.error(f"Error del Servidor: Código {res.status_code}")
                    st.code(res.text)
    else:
        st.warning("⚠️ Por favor ingrese un DNI válido de 8 dígitos numéricos.")

st.markdown("---")
st.caption("DataAPI Interface - Implementación Consulta C4 Premiun")
