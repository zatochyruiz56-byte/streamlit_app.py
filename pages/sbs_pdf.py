import streamlit as st
import requests

def run():
    st.title("🛠️ Diagnóstico de Emergencia: SBS")
    
    TOKEN = "sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"
    dni = st.text_input("DNI para rescatar info", value="45106211")

    if st.button("PROBAR CONEXIÓN CRUDA"):
        url = "https://seeker-v6.com/personas/sbs_pdf_api"
        headers = {
            "Authorization": f"Bearer {TOKEN}",
            "Content-Type": "application/json"
        }
        payload = {"dni": str(dni)}

        st.info("Solicitando datos... (Esperando hasta 2 minutos)")
        
        try:
            # Timeout muy largo para reportes pesados
            res = requests.post(url, headers=headers, json=payload, timeout=120)
            
            st.write(f"📊 **Código HTTP:** {res.status_code}")
            
            # Intentamos ver si es JSON
            try:
                data = res.json()
                st.success("✅ ¡Respuesta JSON recibida!")
                st.json(data)
                
                if "pdf" in data or ("data" in data and "pdf" in data["data"]):
                    st.balloons()
                    st.write("🔥 **PDF DETECTADO.** El código base64 está arriba.")
            except:
                st.warning("⚠️ La respuesta NO es JSON. Mostrando contenido HTML/Texto:")
                # Esto nos mostrará la página de error que viste en la captura
                st.code(res.text)
                
        except requests.exceptions.Timeout:
            st.error("💥 ERROR: El servidor de Seeker tardó más de 2 minutos en responder.")
        except Exception as e:
            st.error(f"💥 Error inesperado: {str(e)}")

run()
