import streamlit as st
import requests

# 1. Verificación de Seguridad
if not st.session_state.get('auth', False):
    st.error("⚠️ Acceso no autorizado. Regrese al Login.")
    st.stop()

# 2. Estilo Visual (Tarjetas y Botones)
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    .status-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("👤 Módulo de Consultas: Personas")
st.write("Seleccione el tipo de consulta que desea realizar:")

# 3. Diseño de Opciones (Columnas)
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="status-card">', unsafe_allow_html=True)
    st.subheader("💎 Servicios Premium")
    
    opcion_premium = st.selectbox("Tipo de búsqueda Premium:", 
                                ["DNI Premium", "Nombres Premium (Próximamente)"])
    
    dni_input = st.text_input("Ingrese DNI para consulta Premium:", max_chars=8)
    
    if st.button("EJECUTAR CONSULTA PREMIUM", use_container_width=True):
        if len(dni_input) == 8:
            TOKEN = "sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"
            URL = "https://seeker-v6.com/personas/apiPremium/dni"
            with st.spinner("Consultando API Premium..."):
                try:
                    r = requests.post(URL, headers={"Authorization": f"Bearer {TOKEN}"}, data={"dni": dni_input})
                    if r.status_code == 200:
                        st.success("✅ Información Encontrada")
                        st.json(r.json()) # Aquí se verá toda la info de la API
                    else:
                        st.error(f"Error en servidor: {r.status_code}")
                except Exception as e:
                    st.error(f"Fallo de conexión: {e}")
        else:
            st.warning("Ingrese un DNI válido de 8 dígitos.")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="status-card">', unsafe_allow_html=True)
    st.subheader("🆓 Servicios Gratuitos")
    
    opcion_gratis = st.selectbox("Tipo de búsqueda Gratis:", 
                               ["DNI Gratis", "Nombres Gratis"])
    
    st.text_input("Ingrese dato (Gratis):", disabled=True, placeholder="Próximamente...")
    
    if st.button("CONSULTA GRATUITA", disabled=True, use_container_width=True):
        pass
    st.info("💡 Las opciones gratuitas se activarán pronto.")
    st.markdown('</div>', unsafe_allow_html=True)

# 4. Botón de retorno
if st.button("🔙 Volver al Panel Principal"):
    st.switch_page("app.py")
