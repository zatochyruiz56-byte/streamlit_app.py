import streamlit as st
import requests

def run():
    st.subheader("🛠️ Diagnóstico de Ficha RENIEC")
    
    TOKEN = "sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"
    dni = st.text_input("DNI para probar")

    if st.button("PROBAR CONEXIÓN"):
        url = "https://seeker-v6.com/personas/api/ficha"
        headers = {
            "Authorization": f"Bearer {TOKEN}",
            "Content-Type": "application/json"
        }
        payload = {"dni": dni}

        # Probamos con POST
        res = requests.post(url, headers=headers, json=payload)
        
        st.write(f"**Código HTTP:** {res.status_code}")
        
        try:
            st.write("**Respuesta Cruda del Servidor:**")
            st.json(res.json()) # Aquí veremos el error real
        except:
            st.write("**Texto recibido (No es JSON):**")
            st.code(res.text)

run()
