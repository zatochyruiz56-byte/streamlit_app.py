import streamlit as st
import requests
import time

# --- CONFIGURACIÓN ---
API_URL = "https://seeker-v6.com/personas/api/consultapremiunc4"
API_TOKEN = "sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"

def realizar_consulta_c4(dni):
    """
    Realiza la petición con cabeceras de navegador para evitar bloqueos.
    """
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json",
        # Añadimos User-Agent para que la API no nos bloquee como simple script de Python
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Accept": "application/json"
    }
    payload = {"dni": str(dni)}
    
    try:
        # Aumentamos el timeout a 25 segundos ya que RENIEC suele ser lento
        response = requests.post(API_URL, headers=headers, json=payload, timeout=25)
        return response
    except requests.exceptions.Timeout:
        return "Error: Tiempo de espera agotado. El servidor de RENIEC está tardando demasiado."
    except Exception as e:
        return f"Error de conexión: {str(e)}"

# --- INTERFAZ STREAMLIT ---
st.set_page_config(page_title="C4 Premiun - DataAPI", page_icon="📑", layout="centered")

# Estilo personalizado para el error
st.markdown("""
    <style>
    .reportview-container { background: #0e1117; }
    .stButton>button { border-radius: 10px; height: 3em; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("📑 Consulta C4 Premiun")
st.info("Nota: Si recibes 'Error al conectar con el servidor', es probable que el servicio de RENIEC esté en mantenimiento temporal. Intenta de nuevo en unos minutos.")

dni = st.text_input("Ingrese DNI de 8 dígitos:", max_chars=8)

if st.button("🚀 REALIZAR CONSULTA", use_container_width=True):
    if len(dni) == 8 and dni.isdigit():
        with st.status("Conectando con DataAPI y RENIEC...", expanded=True) as status:
            res = realizar_consulta_c4(dni)
            
            if isinstance(res, str):
                st.error(res)
            else:
                data = res.json()
                status.update(label="Consulta finalizada", state="complete")
                
                if data.get("status") == "success":
                    st.success("✅ Información obtenida correctamente")
                    
                    # Mostrar créditos en la barra lateral
                    if "creditos_restantes" in data:
                        st.sidebar.metric("Créditos Disponibles", data["creditos_restantes"])
                    
                    # Mostrar datos principales de forma limpia
                    if "data" in data and data["data"]:
                        st.subheader("📋 Datos del Ciudadano")
                        st.json(data["data"])
                    else:
                        st.warning("La API no devolvió datos específicos para este DNI.")
                
                elif "Error al conectar con el servidor" in str(data.get("message", "")):
                    st.error("❌ El proveedor (Seeker-V6) no pudo conectar con RENIEC. Esto es un fallo temporal de su sistema. Por favor, intenta de nuevo en 5 o 10 minutos.")
                    st.expander("Ver respuesta técnica").json(data)
                
                else:
                    st.warning(f"Aviso: {data.get('message', 'Error desconocido')}")
                    st.json(data)
    else:
        st.warning("⚠️ El DNI debe tener exactamente 8 números.")

st.divider()
st.caption("Powered by Seeker-V6 DataAPI | Sistema de Consulta C4")
