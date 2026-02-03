import streamlit as st
import requests

def run():
    st.title("🛠️ Diagnóstico Crudo: Denuncias")
    
    TOKEN = "sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"
    search_value = st.text_input("DNI o Placa para test", value="48694322")
    tipo = st.selectbox("Tipo", ["DNI", "PLACA"])

    if st.button("VER RESPUESTA REAL DEL SERVIDOR"):
        url = "https://seeker-v6.com/personas/apidenuncias"
        headers = {"Authorization": f"Bearer {TOKEN}"}
        params = {"searchValue": search_value, "tipo": tipo}

        st.info(f"Enviando GET a: {url}")
        
        try:
            # Al ser GET, los parámetros van en la URL
            res = requests.get(url, headers=headers, params=params, timeout=30)
            
            st.metric("Código HTTP", res.status_code)
            
            st.subheader("Cuerpo de la respuesta:")
            try:
                # Si es JSON, lo mostramos bonito
                st.json(res.json())
            except:
                # Si no es JSON (como el error que te salió antes), mostramos el texto puro
                st.code(res.text)
                
            if res.status_code == 500:
                st.error("🚨 El servidor de Seeker tiene un error interno (500). No es tu código.")
            elif res.status_code == 401:
                st.error("🔑 Error de autorización. Revisa tu Token.")

        except Exception as e:
            st.error(f"Fallo de conexión: {str(e)}")

run()
