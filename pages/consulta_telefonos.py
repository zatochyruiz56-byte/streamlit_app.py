import streamlit as st
import requests

def run():
    st.title("📱 Consulta DB Teléfonos x DNI")
    
    # Datos extraídos de tu documentación cURL
    API_URL = "https://seeker-v6.com/telefonos/dbTelefonoxdni"
    TOKEN = "sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"
    
    dni = st.text_input("Ingrese DNI del titular", max_chars=8)

    if st.button("🚀 EJECUTAR CONSULTA (cURL)"):
        # Estructura idéntica al comando: curl -X POST ... -d '{...}'
        headers = {
            "Authorization": f"Bearer {TOKEN}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "documento": dni,
            "tipo": "dni",
            "validador": "1" # Parámetro solicitado en tu cURL
        }

        try:
            response = requests.post(API_URL, json=payload, headers=headers)
            
            # Verificación de seguridad contra redirecciones HTML
            if "application/json" not in response.headers.get("Content-Type", ""):
                st.error("❌ El servidor rechazó la conexión API y envió un archivo HTML (Login).")
                st.info("💡 Esto confirma que tu token no tiene permisos para el módulo 'DB Teléfonos'.")
                return

            data = response.json()
            
            if data.get("status") == "success":
                st.success("✅ Datos recuperados")
                st.table(data.get("data"))
            else:
                st.warning(f"Respuesta de la API: {data.get('message')}")

        except Exception as e:
            st.error(f"Error de red: {e}")

if __name__ == "__main__":
    run()
