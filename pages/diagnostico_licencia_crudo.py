import streamlit as st
import requests

st.title("🚗 Seeker v6: Ultra-Debug Mode")

# Configuración
TOKEN = "sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"
DNI = st.text_input("DNI a consultar", value="60799566")

# Intentaremos estas dos URLs
urls_a_probar = [
    "https://seeker-v6.com/api/v1/vehiculos/licencia_conductor",
    "https://seeker-v6.com/vehiculos/licencia_conductor"
]

if st.button("EJECUTAR BÚSQUEDA INTELIGENTE"):
    success = False
    for url in urls_a_probar:
        # ESCAPING FIX: Both backticks below must be escaped (`) to prevent terminating the outer JS template literal.
        st.write(f"Probando: `{url}`...")
        
        headers = {
            "Authorization": f"Bearer {TOKEN}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            # Esto engaña al servidor para que no crea que es un bot de Python
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        
        payload = {"dni": DNI, "tipo": "dni"}
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=10)
            
            # Si es JSON, ¡ganamos!
            try:
                data = response.json()
                st.success(f"🎯 ¡CONECTADO! URL correcta: {url}")
                st.json(data)
                success = True
                break
            except:
                st.warning(f"⚠️ La URL {url} devolvió HTML en lugar de JSON.")
                # Mostramos un pedazo de lo que devolvió para investigar
                if "<title>" in response.text:
                    title = response.text.split('<title>')[1].split('</title>')[0]
                    st.info(f"Título de la página recibida: **{title}**")
                
        except Exception as e:
            st.error(f"Error en esta URL: {str(e)}")
            
    if not success:
        st.error("❌ Ninguna URL funcionó. Es posible que el servidor tenga una protección anti-bots muy fuerte o tu token no tenga permisos.")
