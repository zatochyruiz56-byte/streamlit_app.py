import streamlit as st
import requests

# 1. Configuración de página
st.set_page_config(page_title="DataAPI - Ficha de Persona", layout="wide")

# 2. Estilo CSS para los "Cajoncitos" (Diseño idéntico a la original)
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    .info-container {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 10px;
        min-height: 60px;
    }
    .info-label {
        color: #8b949e;
        font-size: 0.75rem;
        text-transform: uppercase;
        margin-bottom: 4px;
    }
    .info-value {
        color: #ffffff;
        font-size: 1rem;
        font-weight: 600;
    }
    .foto-box {
        border: 2px solid #30363d;
        border-radius: 10px;
        padding: 5px;
        background-color: #000;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

if not st.session_state.get('auth', False):
    st.warning("⚠️ Sesión no iniciada")
    st.stop()

# --- INTERFAZ DE BÚSQUEDA ---
st.title("👤 Consulta de Persona")

col_search1, col_search2 = st.columns([2, 1])
with col_search1:
    dni_input = st.text_input("Número de DNI:", max_chars=8, placeholder="8 dígitos...")

with col_search2:
    st.write("##") # Espaciador
    buscar = st.button("BUSCAR AHORA", use_container_width=True)

if buscar:
    if len(dni_input) == 8:
        TOKEN = "sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"
        URL = "https://seeker-v6.com/personas/apiPremium/dni"
        
        with st.spinner("Generando ficha técnica..."):
            try:
                r = requests.post(URL, headers={"Authorization": f"Bearer {TOKEN}"}, data={"dni": dni_input})
                res = r.json()
                
                if res.get("status") == "success":
                    data = res.get("data", {})
                    
                    st.success("Información recuperada con éxito")
                    st.markdown("---")
                    
                    # --- DISEÑO DE LA FICHA ---
                    col_izq, col_der = st.columns([1, 3])
                    
                    with col_izq:
                        st.markdown('<div class="foto-box">', unsafe_allow_html=True)
                        foto = data.get("foto") or data.get("foto_base64")
                        if foto:
                            st.image(foto, use_container_width=True)
                        else:
                            st.write("📷 SIN FOTO")
                        st.markdown('</div>', unsafe_allow_html=True)
                        st.markdown(f"**DNI: {dni_input}**")

                    with col_der:
                        # Fila 1: Nombres y Apellidos
                        f1c1, f1c2, f1c3 = st.columns(3)
                        for col, lab, val in zip([f1c1, f1c2, f1c3], 
                                               ["NOMBRES", "APELLIDO PATERNO", "APELLIDO MATERNO"],
                                               [data.get("nombres"), data.get("apellido_paterno"), data.get("apellido_materno")]):
                            col.markdown(f'<div class="info-container"><div class="info-label">{lab}</div><div class="info-value">{val or "---"}</div></div>', unsafe_allow_html=True)
                        
                        # Fila 2: Nacimiento y Estado
                        f2c1, f2c2, f2c3 = st.columns(3)
                        for col, lab, val in zip([f2c1, f2c2, f2c3], 
                                               ["FECHA NACIMIENTO", "ESTADO CIVIL", "SEXO"],
                                               [data.get("fecha_nacimiento"), data.get("estado_civil"), data.get("sexo")]):
                            col.markdown(f'<div class="info-container"><div class="info-label">{lab}</div><div class="info-value">{val or "---"}</div></div>', unsafe_allow_html=True)

                        # Fila 3: Ubicación
                        f3c1, f3c2, f3c3 = st.columns(3)
                        for col, lab, val in zip([f3c1, f3c2, f3c3], 
                                               ["DEPARTAMENTO", "PROVINCIA", "DISTRITO"],
                                               [data.get("departamento"), data.get("provincia"), data.get("distrito")]):
                            col.markdown(f'<div class="info-container"><div class="info-label">{lab}</div><div class="info-value">{val or "---"}</div></div>', unsafe_allow_html=True)

                        # Fila 4: Dirección Completa
                        st.markdown(f'<div class="info-container"><div class="info-label">DIRECCIÓN</div><div class="info-value">{data.get("direccion") or "---"}</div></div>', unsafe_allow_html=True)

                    # --- SECCIÓN PADRES ---
                    st.subheader("👪 Datos de los Padres")
                    p1, p2 = st.columns(2)
                    p1.markdown(f'<div class="info-container"><div class="info-label">PADRE</div><div class="info-value">{data.get("nombre_padre") or "---"}</div></div>', unsafe_allow_html=True)
                    p2.markdown(f'<div class="info-container"><div class="info-label">MADRE</div><div class="info-value">{data.get("nombre_madre") or "---"}</div></div>', unsafe_allow_html=True)

                else:
                    st.error(f"❌ {res.get('message', 'DNI no encontrado')}")
            except Exception as e:
                st.error(f"Error técnico: {e}")
    else:
        st.warning("Ingrese 8 dígitos")

if st.button("🔙 VOLVER AL PANEL"):
    st.switch_page("app.py")
