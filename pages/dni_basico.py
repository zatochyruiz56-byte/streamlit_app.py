import streamlit as st
import requests

# 1. Configuración básica
st.set_page_config(page_title="DNI Básico Fixed", layout="wide")

# 2. Función de búsqueda segura
def obtener_dato(diccionario, llaves):
    for llave in llaves:
        valor = diccionario.get(llave)
        if valor and str(valor).strip().lower() not in ["none", "null", ""]:
            return str(valor).upper()
    return "N/D"

# 3. Interfaz Lateral
st.sidebar.title("🔍 Buscador")
dni_input = st.sidebar.text_input("Ingrese DNI (8 dígitos)", max_chars=8)

if st.sidebar.button("BUSCAR AHORA", type="primary", use_container_width=True):
    URL = "https://seeker-v6.com/personas/apiBasico/dni"
    HEADERS = {"Authorization": "Bearer sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"}
    try:
        r = requests.post(URL, headers=HEADERS, data={"dni": dni_input})
        st.session_state.busqueda = r.json()
    except Exception as e:
        st.error(f"Error de conexión: {e}")

if st.sidebar.button("🏠 VOLVER AL INICIO"):
    st.switch_page("app.py")

# 4. Mostrar Resultados
if "busqueda" in st.session_state:
    res = st.session_state.busqueda
    
    # --- MODO DEBUG (IMPORTANTE) ---
    with st.expander("🛠️ VER RESPUESTA CRUDA DE LA API (Analiza los nombres aquí)"):
        st.json(res)
    
    if res.get("status") == "success":
        data = res.get("data", {})
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("📋 Datos Personales")
            
            # Definimos los campos y las posibles llaves que envía la API
            campos = [
                ("Nombres", ["nombres", "nombre", "names"]),
                ("Ap. Paterno", ["paterno", "apellidoPaterno", "ap_paterno"]),
                ("Ap. Materno", ["materno", "apellidoMaterno", "ap_materno"]),
                ("DNI / Doc", ["dni", "numeroDocumento", "documento"]),
                ("Cód. Verif", ["digitoVerificacion", "codVerifica"])
            ]
            
            for label, llaves in campos:
                valor = obtener_dato(data, llaves)
                st.write(f"**{label}:** {valor}")
            
            creditos = obtener_dato(res, ["creditos_restantes", "creditos"])
            st.metric("Créditos Restantes", creditos)

        with col2:
            st.subheader("📷 Foto")
            foto = obtener_dato(data, ["foto", "foto_base64", "fotografia"])
            if foto != "N/D":
                if not foto.startswith("data:"):
                    foto = f"data:image/jpeg;base64,{foto}"
                st.image(foto, use_container_width=True)
            else:
                st.info("No se encontró fotografía")
    else:
        st.error(f"La API dice: {res.get('message', 'Error desconocido')}")
