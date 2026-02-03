import streamlit as st
import requests

st.set_page_config(page_title="Auth Debugger Pro", layout="wide")

st.title("🛡️ Seeker v6: Brute-Force Auth Debugger")
st.write("Probando variaciones de autenticación para la URL oficial.")

url = st.text_input("URL Oficial", value="https://seeker-v6.com/vehiculos/licencia_conductor")
token = st.text_input("Tu Token sk_live", value="sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad")
dni = st.text_input("DNI", value="60799566")

if st.button("PROBAR TODAS LAS COMBINACIONES"):
    # Definimos diferentes formas de enviar el token
    variaciones_headers = [
        {"name": "Standard Bearer", "headers": {"Authorization": f"Bearer {token}"}},
        {"name": "Simple Authorization", "headers": {"Authorization": token}},
        {"name": "Token Header", "headers": {"Token": token}},
        {"name": "X-API-KEY Header", "headers": {"x-api-key": token}},
        {"name": "Key Header", "headers": {"key": token}},
    ]

    for v in variaciones_headers:
        with st.expander(f"Método: {v['name']}", expanded=False):
            try:
                # Añadimos Content-Type y Accept JSON para forzar respuesta de API
                headers = v['headers']
                headers.update({
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0"
                })
                
                # Intentamos con POST
                r = requests.post(url, headers=headers, json={"dni": dni}, timeout=10)
                
                st.write(f"**Status:** {r.status_code}")
                
                # Si el servidor responde con JSON, ¡LO LOGRAMOS!
                try:
                    data = r.json()
                    st.success(f"🎯 ¡ÉXITO! El método '{v['name']}' es el correcto.")
                    st.json(data)
                    st.balloons()
                except:
                    if "Login Seeker" in r.text:
                        st.error("❌ RECHAZADO: El servidor ignoró este header y mostró el Login.")
                    else:
                        st.warning("Respuesta extraña (No es JSON ni Login).")
                        st.text(r.text[:500])
                        
            except Exception as e:
                st.error(f"Error: {str(e)}")

st.divider()
st.info("""
**Nota importante:** Si todos los métodos fallan y muestran 'RECHAZADO', significa que la URL 
'https://seeker-v6.com/vehiculos/licencia_conductor' **NO ES UNA API**, sino una página web 
exclusiva para navegadores (con cookies). 

En ese caso, busca en tu panel de Seeker una sección que diga **'Documentación API'** o **'API para Desarrolladores'**, 
porque la dirección debe ser distinta (ejemplo: 'api.seeker-v6.com').
""")
