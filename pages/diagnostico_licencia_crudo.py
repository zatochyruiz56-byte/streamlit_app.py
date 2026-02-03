import streamlit as st
import requests

st.set_page_config(page_title="Auth Debugger", layout="wide")

st.title("🔑 Validador de Token Seeker")
st.write("Estamos analizando por qué el servidor te pide Login.")

token = st.text_input("Token sk_live", value="sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad")
dni = "60799566"

if st.button("CORRER DIAGNÓSTICO DE RUTA"):
    # Probamos dos posibles URLs
    endpoints = [
        "https://seeker-v6.com/vehiculos/licencia_conductor",
        "https://seeker-v6.com/api/vehiculos/licencia_conductor" # Variante común
    ]
    
    for url in endpoints:
        st.subheader(f"Probando: {url}")
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0"
        }
        
        try:
            # allow_redirects=False es CLAVE: queremos ver el error antes de que nos mande al login
            r = requests.post(url, headers=headers, json={"dni": dni}, allow_redirects=False, timeout=15)
            
            st.code(f"Status Code: {r.status_code}")
            
            if r.status_code in [301, 302]:
                target = r.headers.get("Location")
                st.warning(f"🚨 REDIRECCIÓN DETECTADA: El servidor te intentó mandar a: {target}")
                st.info("Esto significa que el Token NO FUE ACEPTADO para esta ruta.")
            
            elif r.status_code == 401:
                st.error("❌ TOKEN INVÁLIDO: El servidor dice explícitamente que el token no sirve.")
                
            elif r.status_code == 200:
                st.success("✅ ¡CONEXIÓN EXITOSA! Esta es la ruta correcta.")
                try:
                    st.json(r.json())
                except:
                    st.write("La respuesta no es JSON, es texto:")
                    st.text(r.text[:500])
            else:
                st.error(f"Error desconocido: {r.status_code}")
                st.write(r.text[:300])
                
        except Exception as e:
            st.error(f"Fallo al conectar a {url}: {str(e)}")

st.divider()
st.markdown("""
### 💡 Pasos a seguir si sale 'Login Seeker':
1. **Revisa la documentación:** Asegúrate de que la URL no sea `https://api.seeker-v6.com/...`
2. **Token expirado:** Confirma en tu panel de Seeker que el token `sk_live` sigue activo.
3. **Whitelist de IP:** Algunos servidores bloquean las IPs de Streamlit.
""")

