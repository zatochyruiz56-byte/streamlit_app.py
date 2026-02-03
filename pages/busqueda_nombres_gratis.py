import streamlit as st
import requests

st.set_page_config(page_title="API Explorer", layout="wide")

st.title("🔍 Explorador Inteligente de API")
st.write("Probaremos 4 combinaciones de nombres de campos para ver cuál acepta la API.")

n = st.text_input("Nombre a buscar", value="alex")
p = st.text_input("Apellido Paterno", value="ruiz")

if st.button("INICIAR ESCANEO DE PARÁMETROS", type="primary"):
    URL = "https://seeker-v6.com/personas/apiBasico/nombresApellidos"
    TOKEN = "sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"
    HEADERS = {"Authorization": f"Bearer {TOKEN}"}

    # Definimos 4 variantes de parámetros comunes
    variantes = [
        {"nombres": n, "paterno": p, "materno": "", "edadMin": "0", "edadMax": "100"},
        {"nombre": n, "apellido_paterno": p, "apellido_materno": ""},
        {"nombres": n, "apellidoPaterno": p, "apellidoMaterno": ""},
        {"nombres": n, "paterno": p} # Versión mínima
    ]

    cols = st.columns(4)
    
    for i, payload in enumerate(variantes):
        with cols[i]:
            st.info(f"Variante {i+1}")
            st.caption(f"Enviando: {list(payload.keys())}")
            try:
                # Probamos modo data (Formulario) que es el más común
                r = requests.post(URL, headers=HEADERS, data=payload, timeout=5)
                res = r.json()
                
                if res.get("status") == "success" or "data" in res:
                    st.success("✅ ¡FUNCIONA!")
                    st.json(res)
                else:
                    st.error("❌ Error Interno")
                    st.json(res)
            except Exception as e:
                st.error("Error técnico")

