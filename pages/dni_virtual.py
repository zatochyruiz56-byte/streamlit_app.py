import streamlit as st
import requests

def run():
    st.subheader("🛠️ Diagnóstico de Parámetros: DNI Virtual")
    
    TOKEN = "sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"
    dni = st.text_input("DNI para prueba rápida", value="45106211")
    
    # Probamos las 4 variaciones que la API suele aceptar
    tipo_test = st.selectbox("Variación de 'Tipo' a probar", 
                             ["azul", "electronico", "AZUL", "ELECTRONICO"])

    if st.button("PROBAR LLAMADA AHORA"):
        url = "https://seeker-v6.com/personas/virtualdni"
        headers = {
            "Authorization": f"Bearer {TOKEN}",
            "Content-Type": "application/json"
        }
        payload = {
            "dni": str(dni),
            "tipo": tipo_test
        }

        st.write("---")
        st.write("📤 **Enviando a la API:**")
        st.json(payload)

        try:
            res = requests.post(url, headers=headers, json=payload)
            st.write(f"📥 **Código de Estado HTTP:** {res.status_code}")
            
            # Aquí veremos el JSON real que envía el servidor
            data = res.json()
            st.write("📄 **Respuesta Cruda del Servidor:**")
            st.json(data)
            
            if "pdf" in data:
                st.success("✅ ¡ÉXITO! Se recibió la cadena PDF.")
            else:
                st.error(f"❌ Falló: {data.get('message', 'Sin mensaje de error')}")
                
        except Exception as e:
            st.error(f"💥 Error de conexión: {e}")

run()
