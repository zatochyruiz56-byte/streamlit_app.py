import streamlit as st
import requests

def run():
    st.title("🛠️ Diagnóstico Crudo: TIVE V2")
    
    TOKEN = "sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"
    placa = st.text_input("Placa para test", value="24145T").upper()

    if st.button("VER RESPUESTA REAL DEL SERVIDOR"):
        url = "https://seeker-v6.com/vehiculos/api_tive_v2"
        headers = {"Authorization": f"Bearer {TOKEN}"}
        payload = {"placa": placa}

        st.info(f"Enviando POST a: {url} con placa: {placa}")
        
        try:
            # Según doc, este es un POST
            res = requests.post(url, headers=headers, json=payload, timeout=30)
            
            st.metric("Código HTTP", res.status_code)
            st.write(f"**Content-Type:** {res.headers.get('Content-Type')}")
            
            st.subheader("Contenido de la respuesta:")
            
            # Si el Content-Type no es JSON, Seeker está fallando
            if "application/json" in res.headers.get("Content-Type", ""):
                try:
                    st.json(res.json())
                except:
                    st.error("Error al decodificar JSON.")
                    st.code(res.text)
            else:
                st.warning("⚠️ El servidor NO respondió con datos. Respondió con HTML (posible página de error/login):")
                # Esto es lo que causó tu "Error de Sesión"
                st.code(res.text[:2000]) 

        except Exception as e:
            st.error(f"Fallo de conexión: {str(e)}")

if __name__ == "__main__":
    run()
