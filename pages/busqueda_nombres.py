import streamlit as st
import requests

# 1. Configuración
st.set_page_config(page_title="Búsqueda por Nombres - Premium", layout="wide")

# 2. Estilo Premium (Cajones Oscuros)
st.markdown("""
<style>
    .stApp { background-color: #0e1117; }
    .premium-title { color: #00a36c; font-size: 24px; font-weight: bold; margin-bottom: 20px; display: flex; align-items: center; gap: 10px; }
    .data-card { background-color: #161b22; border-radius: 8px; border: 1px solid #30363d; overflow: hidden; margin-bottom: 25px; }
    .data-row { display: flex; border-bottom: 1px solid #30363d; padding: 14px 20px; align-items: center; background-color: #161b22; }
    .data-row:last-child { border-bottom: none; }
    .data-label { width: 45%; color: #8b949e; font-size: 11px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.5px; }
    .data-value { width: 55%; color: #ffffff; font-weight: 700; font-size: 14px; }
    
    /* Foto */
    .photo-label { color: #8b949e; font-size: 11px; font-weight: bold; text-align: center; margin-bottom: 10px; }
    .photo-frame { border: 2px solid #30363d; border-radius: 12px; padding: 40px 20px; background: #161b22; text-align: center; }
    .no-photo-text { color: #8b949e; font-size: 13px; font-weight: bold; }

    #MainMenu, footer, header {visibility: hidden;}
    .stButton>button { border-radius: 8px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

def val(d, keys):
    if not isinstance(d, dict): return "N/D"
    for k in keys:
        v = d.get(k)
        if v and str(v).strip().lower() not in ["none", "null", ""]:
            return str(v).upper()
    return "N/D"

# --- FORMULARIO DE BÚSQUEDA ---
with st.sidebar:
    st.markdown("<h2 style='text-align:center;'>🔍 FILTROS</h2>", unsafe_allow_html=True)
    nombre = st.text_input("NOMBRES")
    paterno = st.text_input("APELLIDO PATERNO")
    materno = st.text_input("APELLIDO MATERNO")
    
    col_e1, col_e2 = st.columns(2)
    e_min = col_e1.text_input("EDAD MÍN", value="0")
    e_max = col_e2.text_input("EDAD MÁX", value="100")
    
    if st.button("EJECUTAR CONSULTA", type="primary", use_container_width=True):
        if nombre or paterno or materno:
            URL = "https://seeker-v6.com/personas/apiPremium/nombres"
            HEADERS = {"Authorization": "Bearer sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"}
            PAYLOAD = {
                "name": nombre,
                "appPaterno": paterno,
                "appMaterno": materno,
                "edadMin": e_min,
                "edadMax": e_max
            }
            try:
                r = requests.post(URL, headers=HEADERS, data=PAYLOAD)
                st.session_state.res_nombres = r.json()
            except: st.error("Error al conectar con el servidor")
        else:
            st.warning("Ingrese al menos un nombre o apellido")

    if st.button("🏠 MENÚ PRINCIPAL", use_container_width=True):
        st.switch_page("app.py")

# --- RESULTADOS ---
if "res_nombres" in st.session_state:
    res = st.session_state.res_nombres
    if res.get("status") == "success":
        data = res.get("data", [])
        if not data:
            st.warning("No se encontraron personas con esos criterios.")
        else:
            st.markdown(f'<div class="premium-title">👥 Personas Encontradas ({len(data)})</div>', unsafe_allow_html=True)
            
            for persona in data:
                c1, c2 = st.columns([2, 1])
                with c1:
                    fields = [
                        ("DNI / DOCUMENTO", ["dni", "numeroDocumento"]),
                        ("NOMBRES", ["nombres", "nombre"]),
                        ("APELLIDO PATERNO", ["ap_paterno", "paterno", "appPaterno"]),
                        ("APELLIDO MATERNO", ["ap_materno", "materno", "appMaterno"]),
                        ("FECHA NAC.", ["fechaNacimiento", "nacimiento"]),
                        ("GÉNERO", ["sexo", "genero"]),
                    ]
                    
                    html = '<div class="data-card">'
                    for label, keys in fields:
                        valor = val(persona, keys)
                        html += f'<div class="data-row"><div class="data-label">{label}</div><div class="data-value">{valor}</div></div>'
                    html += '</div>'
                    st.markdown(html, unsafe_allow_html=True)
                
                with c2:
                    st.markdown('<div class="photo-label">BIOMETRÍA</div>', unsafe_allow_html=True)
                    st.markdown('<div class="photo-frame"><div class="no-photo-text">NO DISPONIBLE</div><div style="font-size:40px; margin-top:10px; opacity:0.2;">👤</div></div>', unsafe_allow_html=True)
                
                st.markdown("<hr style='border-color: #30363d; margin-bottom: 30px;'>", unsafe_allow_html=True)
    else:
        st.error("Error en la consulta o créditos insuficientes.")
else:
    st.info("Utilice los filtros laterales para realizar una búsqueda premium por nombres.")
