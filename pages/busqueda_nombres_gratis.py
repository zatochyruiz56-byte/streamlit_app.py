import streamlit as st
import requests

st.set_page_config(page_title="Debug API", layout="centered")

st.title("🛠️ Extractor de Datos Crudos")
st.info("Introduce los datos abajo para ver la respuesta real de la API.")

with st.form("debug_form"):
    n = st.text_input("Nombres (ej: alex)")
    p = st.text_input("Apellido Paterno (ej: ruiz)")
    m = st.text_input("Apellido Materno")
    submit = st.form_submit_button("OBTENER JSON CRUDO", use_container_width=True)

if submit:
    URL = "https://seeker-v6.com/personas/apiBasico/nombresApellidos"
    HEADERS = {"Authorization": "Bearer sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"}
    DATA = {
        "nombres": n, 
        "paterno": p, 
        "materno": m, 
        "edadMin": "0", 
        "edadMax": "100"
    }
    
    try:
        with st.spinner("Consultando API..."):
            r = requests.post(URL, headers=HEADERS, data=DATA)
            resultado_json = r.json()
            
            st.markdown("### 📋 RESULTADO DE LA API:")
            st.json(resultado_json)
            
            st.success("Copia el texto de arriba y pásalo por el chat.")
            
    except Exception as e:
        st.error(f"Error técnico: {str(e)}")
