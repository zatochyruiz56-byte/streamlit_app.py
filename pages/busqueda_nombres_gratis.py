import streamlit as st
import requests

st.set_page_config(page_title="Super Debugger", layout="wide")

st.title("🚀 Super Debugger Multi-Formato")
st.write("Probaremos enviando los datos de dos formas distintas para ver cuál funciona.")

with st.sidebar:
    st.header("Parámetros")
    n = st.text_input("Nombres", value="alex")
    p = st.text_input("Paterno", value="ruiz")
    m = st.text_input("Materno", value="")
    token = "sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"

if st.button("EJECUTAR PRUEBAS DE FUERZA BRUTA", type="primary"):
    URL = "https://seeker-v6.com/personas/apiBasico/nombresApellidos"
    HEADERS = {
        "Authorization": f"Bearer {token}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    PAYLOAD = {"nombres": n, "paterno": p, "materno": m, "edadMin": "0", "edadMax": "100"}

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Prueba 1: Modo JSON")
        try:
            r1 = requests.post(URL, headers=HEADERS, json=PAYLOAD, timeout=10)
            st.code(f"Status: {r1.status_code}")
            st.json(r1.json())
        except Exception as e:
            st.error(f"Error en Prueba 1: {e}")

    with col2:
        st.subheader("Prueba 2: Modo Formulario")
        try:
            r2 = requests.post(URL, headers=HEADERS, data=PAYLOAD, timeout=10)
            st.code(f"Status: {r2.status_code}")
            st.json(r2.json())
        except Exception as e:
            st.error(f"Error en Prueba 2: {e}")

    st.divider()
    st.info("Si ambas dan 'Error Interno', es posible que el servidor de la API esté caído o los parámetros (nombres, paterno, etc) hayan cambiado de nombre.")
