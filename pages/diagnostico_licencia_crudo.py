import streamlit as st
import requests

st.set_page_config(page_title="Endpoint Scanner", layout="wide")

st.title("🔍 Escáner de Rutas Seeker v6")
st.info("El objetivo es encontrar una ruta que devuelva JSON y no HTML.")

token = st.text_input("Token sk_live", value="sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad")
dni = st.text_input("DNI de prueba", value="60799566")

if st.button("INICIAR ESCANEO DE API"):
    # Lista de rutas que suelen usar las APIs de Seeker
    rutas_a_probar = [
        "https://seeker-v6.com/api/licencia_conductor",
        "https://seeker-v6.com/api/v1/vehiculos/licencia_conductor",
        "https://api.seeker-v6.com/vehiculos/licencia_conductor",
        "https://seeker-v6.com/api/v2/licencia_conductor",
        "https://seeker-v6.com/vehiculos/licencia_conductor" # Tu ruta actual (para comparar)
    ]
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json", # IMPORTANTE: Pedimos JSON explícitamente
        "User-Agent": "Mozilla/5.0"
    }
    
    for url in rutas_a_probar:
        with st.expander(f"Probando: {url}", expanded=False):
            try:
                r = requests.post(url, headers=headers, json={"dni": dni}, timeout=10)
                
                st.write(f"**Status:** {r.status_code}")
                
                # DETECCIÓN DE LOGIN (Falso Positivo)
                if "Login Seeker" in r.text or "<!DOCTYPE html>" in r.text:
                    st.warning("⚠️ ESTO ES UNA WEB, NO UNA API. (Te mandó al Login)")
                
                # DETECCIÓN DE DATOS REALES
                try:
                    data = r.json()
                    st.success("🎯 ¡ENCONTRADO! Esta ruta devuelve JSON real.")
                    st.json(data)
                    st.balloons()
                except:
                    st.error("No es JSON. Es texto plano o HTML.")
                    if r.status_code == 200:
                        st.text_area("Contenido recibido (Primeros 200 caracteres):", r.text[:200])

            except Exception as e:
                st.error(f"Error de conexión: {str(e)}")

st.markdown("""
---
### 🚦 Guía de Resultados
- **Ruta con Login:** Es para humanos, no para tu código.
- **Ruta con JSON:** Es la que debes usar en tu aplicación final.
- **Status 404:** Esa dirección no existe en el servidor.
""")
