mport streamlit as st
import requests

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="DNI Básico DEBUGGER", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #0d1117; }
    .main-card { background: #161b22; border: 1px solid #30363d; border-radius: 12px; padding: 20px; }
    .info-table { width: 100%; border-collapse: collapse; margin-top: 10px; }
    .info-table td { padding: 12px; border-bottom: 1px solid #21262d; color: #c9d1d9; font-family: sans-serif; }
    .info-table td:first-child { color: #8b949e; font-weight: bold; width: 35%; font-size: 0.7rem; text-transform: uppercase; }
    .json-debug { background: #000; padding: 10px; border-radius: 5px; border-left: 3px solid #3b82f6; font-family: monospace; font-size: 0.8rem; }
</style>
""", unsafe_allow_html=True)

def find_data(obj, keys, default="N/D"):
    if not isinstance(obj, dict): return default
    for k in keys:
        if k in obj and obj[k]:
            val = str(obj[k]).strip()
            if val.lower() not in ["none", "null", ""]: return val.upper()
    return default

c_left, c_right = st.columns([1, 2.5])

with c_left:
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.subheader("🔍 Buscador")
    dni = st.text_input("DNI", max_chars=8)
    
    if st.button("CONSULTAR", type="primary", use_container_width=True):
        URL = "https://seeker-v6.com/personas/apiBasico/dni"
        HEADERS = {"Authorization": "Bearer sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"}
        DATA = {"dni": dni}
        
        try:
            r = requests.post(URL, headers=HEADERS, data=DATA)
            st.session_state.raw_json = r.json()
        except Exception as e:
            st.error(f"Error: {e}")
    
    if st.button("🏠 INICIO"): st.switch_page("app.py")
    st.markdown('</div>', unsafe_allow_html=True)

if 'raw_json' in st.session_state:
    res = st.session_state.raw_json
    
    with c_right:
        # --- EL "F12" DE STREAMLIT ---
        with st.expander("🛠️ VER JSON CRUDO (Aquí ves los nombres reales de las variables)"):
            st.json(res)
            st.info("Revisa arriba si los nombres como 'nombres' o 'paterno' coinciden exactamente.")

        if res.get("status") == "success":
            data = res.get("data", {})
            st.success("Información extraída correctamente")
            
            # Intento de mapeo automático
            campos = [
                ("Nombres", ["nombres", "nombre", "names"]),
                ("Apellido Paterno", ["paterno", "apellidoPaterno", "ap_paterno"]),
                ("Apellido Materno", ["materno", "apellidoMaterno", "ap_materno"]),
                ("DNI", ["dni", "numeroDocumento", "documento"]),
                ("Cód. Verif", ["digitoVerificacion", "codVerifica"]),
                ("Créditos", ["creditos_restantes"])
            ]
            
            html = '<table class="info-table">'
            for label, keys in campos:
                # Buscamos en 'data' o en la raíz 'res'
                val = find_data(data, keys)
                if val == "N/D": val = find_data(res, keys)
                html += f'<tr><td>{label}</td><td style="font-weight:bold;">{val}</td></tr>'
            html += '</table>'
            st.markdown(html, unsafe_allow_html=True)
            
            # Foto
            foto_base64 = find_data(data, ["foto", "foto_base64", "fotografia"], None)
            if foto_base64:
                if not foto_base64.startswith("data:"):
                    foto_base64 = f"data:image/jpeg;base64,{foto_base64}"
                st.image(foto_base64, width=200)
        else:
            st.error(f"Error de la API: {res.get('message', 'Sin mensaje')}")
