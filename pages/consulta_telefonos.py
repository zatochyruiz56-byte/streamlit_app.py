import streamlit as st
import requests

def run():
    st.title("📱 Consulta DB Teléfonos x DNI")
    st.markdown("---")

    # Credenciales y Endpoint según la documentación oficial
    # https://seeker-v6.com/telefonos/dbTelefonoxdni
    API_URL = "https://seeker-v6.com/telefonos/dbTelefonoxdni"
    TOKEN = "sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"
    
    dni_input = st.text_input("Ingrese DNI a consultar", max_chars=8, help="DNI del titular de la línea")

    if st.button("🚀 EJECUTAR CONSULTA (cURL)"):
        if len(dni_input) == 8:
            # Replicando los Headers del cURL
            headers = {
                "Authorization": f"Bearer {TOKEN}",
                "Content-Type": "application/json"
            }
            
            # Replicando el Body (-d) del cURL
            # 'tipo' y 'validador' son opcionales según la documentación
            payload = {
                "documento": dni_input,
                "tipo": "dni",
                "validador": "1" 
            }

            try:
                with st.spinner("Procesando petición POST..."):
                    response = requests.post(API_URL, json=payload, headers=headers)
                    
                    # Verificación de tipo de contenido para evitar el error de HTML/Login
                    if "application/json" not in response.headers.get("Content-Type", ""):
                        st.error("❌ El servidor no respondió con JSON.")
                        st.warning("Esto suele indicar que el servidor te redirigió a la página de Login (Sesión caducada).")
                        return

                    data = response.json()

                if response.status_code == 200 and data.get("status") == "success":
                    st.success("✅ Información obtenida con éxito")
                    
                    # ORGANIZACIÓN EN PLANTILLA
                    st.subheader("📋 Lista de Teléfonos Encontrados")
                    if data.get("data"):
                        # Mostramos los resultados en una tabla limpia
                        st.table(data["data"])
                    else:
                        st.info("No se encontraron registros para este DNI.")
                        
                    if "creditos_restantes" in data:
                        st.sidebar.metric("Saldo", f"{data['creditos_restantes']} créditos")
                
                else:
                    # Captura de errores específicos (Saldo, Token, etc.)
                    msg = data.get("message", "Error desconocido en la API")
                    st.error(f"⚠️ Error: {msg}")

            except Exception as e:
                st.error(f"🔥 Fallo en la conexión: {str(e)}")
        else:
            st.warning("El DNI debe tener exactamente 8 dígitos.")

if __name__ == "__main__":
    run()
