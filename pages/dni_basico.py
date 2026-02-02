import streamlit as st
import requests

# 1. Configuración de página con tema oscuro forzado vía CSS
st.set_page_config(page_title="DNI Básico - Estilo Premium", layout="wide")

# Estilos CSS para replicar la versión Premium
st.markdown("""
<style>
    /* Fondo principal y textos */
    .stApp { background-color: #0e1117; }
    h1, h2, h3, p, span, label { color: white !important; }
    
    /* Estilo del título verde */
    .premium-title {
        color: #00a36c;
        font-size: 28px;
        font-weight: bold;
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 20px;
    }
    
    /* Contenedor de la tabla de datos */
    .data-container {
        background-color: #161b22;
        border-radius: 10px;
        border: 1px solid #30363d;
        padding: 0px;
        overflow: hidden;
    }
    
    /* Filas de la tabla */
    .data-row {
        display: flex;
        border-bottom: 1px solid #30363d;
        padding: 12px 15px;
    }
    .data-label {
        width: 40%;
        color: #8b949e;
        font-size: 13px;
        font-weight: bold;
        text-transform: uppercase;
    }
    .data-value {
        width: 60%;
        color: white;
        font-weight: bold;
        font-size: 15px;
    }
    
    /* Contenedor de Foto */
    .photo-label {
        text-align: center;
        color: #8b949e;
        font-size: 12px;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .photo-container {
        border: 4px solid #30363d;
        border-radius: 15px;
        padding: 10px;
        background: #161b22;
    }
</style>
""", unsafe_allow_stdio=True, unsafe_allow_html=True)

def obtener_dato(diccionario, llaves):
    if not isinstance(diccionario, dict): return "N/D"
    for llave in llaves:
        valor = diccionario.get(llave)
        if valor and str(valor).strip().lower() not in ["none", "null", ""]:
            return str(valor).upper()
    return "N/D"

# --- SIDEBAR ---
st.sidebar.markdown("<h2 style='text-align:center;'>🔍 Buscador</h2>", unsafe_allow_html=True)
dni_input = st.sidebar.text_input("DNI A CONSULTAR", max_chars=8)

if st.sidebar.button("EJECUTAR CONSULTA", type="primary", use_container_width=True):
    URL = "https://seeker-v6.com/personas/apiBasico/dni"
    HEADERS = {"Authorization": "Bearer sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"}
    try:
        r = requests.post(URL, headers=HEADERS, data={"dni": dni_input})
        st.session_state.busqueda = r.json()
    except Exception as e:
        st.error(f"Error: {e}")

if st.sidebar.button("🏠 MENÚ PRINCIPAL", use_container_width=True):
    st.switch_page("app.py")

# --- ÁREA PRINCIPAL ---
if "busqueda" in st.session_state:
    res = st.session_state.busqueda
    
    if res.get("status") == "success":
        data_raw = res.get("data", [])
        data = data_raw[0] if (isinstance(data_raw, list) and len(data_raw) > 0) else (data_raw if isinstance(data_raw, dict) else {})

        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown('<div class="premium-title">📋 Datos Obtenidos</div>', unsafe_allow_html=True)
            
            # Construcción de la tabla estilo Premium
            campos = [
                ("DNI / DOCUMENTO", ["dni", "numeroDocumento"]),
                ("NOMBRES", ["nombres", "nombre"]),
                ("APELLIDO PATERNO", ["ap_paterno", "paterno"]),
                ("APELLIDO MATERNO", ["ap_materno", "materno"]),
                ("CÓD. VERIF", ["digitoVerificacion", "codVerifica"]),
            ]
            
            html_tabla = '<div class="data-container">'
            for label, llaves in campos:
                valor = obtener_dato(data, llaves)
                html_tabla += f'''
                <div class="data-row">
                    <div class="data-label">{label}</div>
                    <div class="data-value">{valor}</div>
                </div>
                '''
            html_tabla += '</div>'
            st.markdown(html_tabla, unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="photo-label">BIOMETRÍA RENIEC</div>', unsafe_allow_html=True)
            foto = obtener_dato(data, ["foto", "foto_base64", "fotografia"])
            
            st.markdown('<div class="photo-container">', unsafe_allow_html=True)
            if foto != "N/D":
                if not foto.startswith("data:"):
                    foto = f"data:image/jpeg;base64,{foto}"
                st.image(foto, use_container_width=True)
            else:
                st.info("SIN FOTO")
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.error(f"Error: {res.get('message', 'Error desconocido')}")
else:
    # Pantalla inicial vacía con estilo
    st.info("Ingrese un DNI en la barra lateral para comenzar.")
