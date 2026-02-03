import streamlit as st
import requests

st.set_page_config(page_title="Seeker Data Extractor", layout="wide")

st.title("🚗 Extractor de Datos: Licencia y Puntos")
st.write("Objetivo: Obtener el JSON que contiene 'Categoría', 'Vencimiento' y 'Puntos'.")

token = st.text_input("Token sk_live", value="sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad")
dni = st.text_input("DNI a consultar", value="60799566")

# Estas son las rutas probables para el JSON de multiconsultas
endpoints = [
    "https://seeker-v6.com/api/vehiculos/multiconsultas",
    "https://seeker-v6.com/api/v1/multiconsultas",
    "https://seeker-v6.com/api/licencias/detalle",
    "https://api.seeker-v6.com/vehiculos/multiconsultas"
]

if st.button("EXTRAER INFORMACIÓN DEL TABLERO"):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0"
    }
    
    found = False
    for url in endpoints:
        with st.status(f"Analizando: {url}...", expanded=True) as status:
            try:
                # Probamos con POST que es lo estándar para estas consultas
                r = requests.post(url, headers=headers, json={"dni": dni}, timeout=12)
                
                if r.status_code == 200 and "application/json" in r.headers.get("Content-Type", ""):
                    data = r.json()
                    status.update(label="✅ DATOS ENCONTRADOS", state="complete")
                    st.success(f"Se encontraron datos en: {url}")
                    st.json(data)
                    found = True
                    st.balloons()
                    break
                else:
                    status.update(label=f"❌ No hay JSON (Status: {r.status_code})", state="error")
                    if "Login Seeker" in r.text:
                        st.warning("Esta URL redirige al Login (es una página web).")
            
            except Exception as e:
                status.update(label="Fallo de conexión", state="error")

    if not found:
        st.error("No se pudo localizar el endpoint de la API. Verifica si el token tiene permisos para 'Multiconsultas'.")

st.divider()
st.markdown("""
### 💡 ¿Qué estamos buscando?
En tus capturas de pantalla, la URL es `/vehiculos/multiconsultas`. 
En una API, esa ruta suele cambiar a `/api/vehiculos/multiconsultas`. 
Si este script falla, significa que Seeker v6 usa un **subdominio** (como `api.seeker-v6.com`) o un **Token diferente** para esa sección.
""")
