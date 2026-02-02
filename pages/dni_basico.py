import streamlit as st
import requests

# 1. Configuración de página con Layout Ancho
st.set_page_config(page_title="Buscador DNI - Estilo Premium", layout="wide")

# 2. Inyección de CSS para Diseño Premium (Fondo oscuro, Acentos verdes)
st.markdown("""
<style>
    /* Estilo General */
    .stApp { background-color: #0e1117; }
    h1, h2, h3, p, span, label, .stMarkdown { color: white !important; }
    
    /* Títulos de Sección */
    .premium-title {
        color: #00a36c;
        font-size: 26px;
        font-weight: bold;
        margin-bottom: 25px;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    /* Contenedor de Tabla de Datos */
    .data-card {
        background-color: #161b22;
        border-radius: 12px;
        border: 1px solid #30363d;
        overflow: hidden;
        margin-top: 10px;
    }
    
    /* Filas de la Tabla */
    .data-row {
        display: flex;
        border-bottom: 1px solid #30363d;
        padding: 14px 18px;
        align-items: center;
    }
    .data-row:last-child { border-bottom: none; }
    
    .data-label {
        width: 45%;
        color: #8b949e;
        font-size: 12px;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .data-value {
        width: 55%;
        color: #ffffff;
        font-weight: 700;
        font-size: 15px;
    }
    
    /* Contenedor de Fotografía */
    .photo-header {
        text-align: center;
        color: #8b949e;
        font-size: 12px;
        font-weight: bold;
        margin-bottom: 12px;
        letter-spacing: 1px;
    }
    .photo-frame {
        border: 4px solid #30363d;
        border-radius: 18px;
        padding: 12px;
        background: #161b22;
        box-shadow: 0 10px 25px rgba(0,0,0,0.5);
    }
    
    /* Ocultar elementos innecesarios */
    #MainMenu, footer, header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Función de ayuda para extraer datos de forma segura
def val(d, keys):
    if not isinstance(d, dict): return "N/D"
    for k in keys:
        v = d.get(k)
        if v and str(v).strip().lower() not in ["none", "null", ""]:
            return str(v).upper()
    return "N/D"

# --- BARRA LATERAL (SIDEBAR) ---
with st.sidebar:
    st.markdown("<h2 style='text-align:center;'>🔍 BUSCADOR</h2>", unsafe_allow_html=True)
    dni_input = st.text_input("DNI A CONSULTAR", max_chars=8, placeholder="Ej: 45106211")
    
    if st.button("EJECUTAR CONSULTA", type="primary", use_container_width=True):
        if len(dni_input) == 8:
            URL = "https://seeker-v6.com/personas/apiBasico/dni"
            HEADERS = {"Authorization": "Bearer sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"}
            try:
                with st.spinner("Consultando..."):
                    r = requests.post(URL, headers=HEADERS, data={"dni": dni_input}, timeout=10)
                    st.session_state.result_basico = r.json()
            except Exception as e:
                st.error(f"Error de red: {e}")
        else:
            st.warning("El DNI debe tener 8 dígitos.")

    if st.button("🏠 MENÚ PRINCIPAL", use_container_width=True):
        st.switch_page("app.py")

# --- ÁREA DE RESULTADOS ---
if "result_basico" in st.session_state:
    res = st.session_state.result_basico
    
    if res.get("status") == "success":
        # Extraer datos (maneja si es lista o dict)
        raw_data = res.get("data", [])
        info = raw_data[0] if (isinstance(raw_data, list) and len(raw_data) > 0) else (raw_data if isinstance(raw_data, dict) else {})

        col_info, col_img = st.columns([1.8, 1])
        
        with col_info:
            st.markdown('<div class="premium-title">📋 Datos Obtenidos</div>', unsafe_allow_html=True)
            
            # Definición de campos para la tabla
            items = [
                ("DNI / DOCUMENTO", ["dni", "numeroDocumento"]),
                ("NOMBRES", ["nombres", "nombre"]),
                ("APELLIDO PATERNO", ["ap_paterno", "paterno"]),
                ("APELLIDO MATERNO", ["ap_materno", "materno"]),
                ("CÓD. VERIF", ["digitoVerificacion", "codVerifica"]),
            ]
            
            # Generar tabla HTML
            html = '<div class="data-card">'
            for label, keys in items:
                valor_final = val(info, keys)
                html += f'''
                <div class="data-row">
                    <div class="data-label">{label}</div>
                    <div class="data-value">{valor_final}</div>
                </div>
                '''
            html += '</div>'
            st.markdown(html, unsafe_allow_html=True)

        with col_img:
            st.markdown('<div class="photo-header">BIOMETRÍA RENIEC</div>', unsafe_allow_html=True)
            foto_data = val(info, ["foto", "foto_base64", "fotografia"])
            
            st.markdown('<div class="photo-frame">', unsafe_allow_html=True)
            if foto_data != "N/D":
                # Asegurar formato base64 correcto
                if not foto_data.startswith("data:"):
                    foto_data = f"data:image/jpeg;base64,{foto_data}"
                st.image(foto_data, use_container_width=True)
            else:
                st.info("No se encontró fotografía en la base de datos.")
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.error(f"Aviso: {res.get('message', 'No se encontraron registros para este DNI.')}")
else:
    # Estado inicial amigable
    st.markdown("""
    <div style="text-align: center; margin-top: 100px; opacity: 0.5;">
        <h2 style="color: #8b949e !important;">LISTO PARA BUSCAR</h2>
        <p>Ingresa un número de documento en el panel izquierdo.</p>
    </div>
    """, unsafe_allow_html=True)
