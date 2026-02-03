import streamlit as st
import requests

# 1. Configuración de pantalla
st.set_page_config(page_title="Búsqueda Básica - DEBUG", layout="wide")

# 2. CSS Estilo Knowlers
st.markdown("""
<style>
    .stApp { background-color: #0b0e14; }
    .results-table-container { width: 100%; border-radius: 4px; overflow: hidden; border: 1px solid #1e293b; margin-top: 20px; }
    table { width: 100%; border-collapse: collapse; font-family: 'Inter', sans-serif; font-size: 11px; color: #cbd5e1; }
    thead tr { background-color: #0076ce !important; }
    th { color: white !important; text-align: left; padding: 12px 10px; text-transform: uppercase; font-weight: 700; border-right: 1px solid rgba(255,255,255,0.1); }
    tbody tr:nth-child(even) { background-color: #161b22; }
    tbody tr:nth-child(odd) { background-color: #0b0e14; }
    td { padding: 10px; border-bottom: 1px solid #1e293b; border-right: 1px solid #1e293b; }
    .premium-tag { color: #facc15; font-size: 9px; font-weight: bold; }
    #MainMenu, footer, header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- PANEL LATERAL ---
with st.sidebar:
    st.markdown("<h2 style='text-align:center;'>🎁 DEBUG GRATIS</h2>", unsafe_allow_html=True)
    n = st.text_input("NOMBRES")
    p = st.text_input("AP. PATERNO")
    m = st.text_input("AP. MATERNO")
    
    st.markdown("---")
    e_min = st.text_input("EDAD MÍN", value="0")
    e_max = st.text_input("EDAD MÁX", value="100")
    
    if st.button("VER INFO CRUDA (DEBUG)", type="primary", use_container_width=True):
        URL = "https://seeker-v6.com/personas/apiBasico/nombresApellidos"
        HEADERS = {"Authorization": "Bearer sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"}
        DATA = {"nombres": n, "paterno": p, "materno": m, "edadMin": e_min, "edadMax": e_max}
        try:
            r = requests.post(URL, headers=HEADERS, data=DATA)
            res = r.json()
            
            # --- MOSTRAR INFORMACIÓN CRUDA AQUÍ ---
            st.markdown("### 🛠️ DATOS CRUDOS RECIBIDOS (Copia esto y pásalo):")
            st.json(res)
            
            if res.get("status") == "success":
                st.session_state.raw_data = res.get("data", [])
            else:
                st.error("Error en la respuesta de la API")
        except Exception as e:
            st.error(f"Error de conexión: {str(e)}")

if "raw_data" in st.session_state:
    st.success(f"Se recibieron {len(st.session_state.raw_data)} resultados. Mira arriba el JSON crudo.")

COPIAR CÓDIGO GRATIS (CON JSON)
MODO DEBUG: Búsqueda Premium
busqueda_nombres_premium.py
import streamlit as st
import requests

st.set_page_config(page_title="Búsqueda Premium - DEBUG", layout="wide")

with st.sidebar:
    st.markdown("## 💎 DEBUG PREMIUM")
    nombre = st.text_input("NOMBRES")
    paterno = st.text_input("AP. PATERNO")
    materno = st.text_input("AP. MATERNO")
    
    if st.button("BUSCAR Y VER JSON"):
        URL = "https://seeker-v6.com/personas/apiPremium/nombres"
        HEADERS = {"Authorization": "Bearer sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"}
        DATA = {"name": nombre, "appPaterno": paterno, "appMaterno": materno, "edadMin": "0", "edadMax": "100"}
        
        r = requests.post(URL, headers=HEADERS, data=DATA)
        res = r.json()
        
        st.markdown("### 💎 JSON PREMIUM:")
        st.json(res)
