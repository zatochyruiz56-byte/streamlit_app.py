import streamlit as st
import requests

def run():
    st.title("📱 Consulta DB Teléfonos x DNI")
    st.info("Este endpoint busca números telefónicos asociados a un documento.")

    # Configuración según la documentación de Seeker-V6
    API_URL = "https://seeker-v6.com/telefonos/dbTelefonoxdni"
    TOKEN = "sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"
    
    dni = st.text_input("Ingrese DNI del titular", max_chars=8)
    
    if st.button("🔍 BUSCAR TELÉFONOS"):
        if len(dni) == 8:
            headers = {
                "Authorization": f"Bearer {TOKEN}",
                "Content-Type": "application/json"
            }
            # Parámetros según la documentación: documento, tipo (opcional), validador (opcional)
            payload = {
                "documento": dni,
                "tipo": "dni"
            }

            try:
                with st.spinner("Consultando base de datos de telefonía..."):
                    response = requests.post(API_URL, json=payload, headers=headers)
                    
                    # Verificamos si es HTML (error de login) o JSON (datos)
                    try:
                        data = response.json()
                    except:
                        st.error("❌ El servidor devolvió un error de sesión (Página de Login).")
                        return

                if response.status_code == 200 and data.get("status") == "success":
                    st.success("✅ Información recuperada")
                    
                    # --- INICIO DE TU PLANTILLA ---
                    st.markdown("### 📋 Resultados de Búsqueda")
                    
                    # Si 'data' es una lista de teléfonos, los mostramos en una tabla limpia
                    if isinstance(data.get("data"), list):
                        st.table(data["data"])
                    else:
                        st.json(data.get("data"))
                    # --- FIN DE TU PLANTILLA ---

                    if "creditos_restantes" in data:
                        st.sidebar.metric("Saldo Actual", f"{data['creditos_restantes']} 🪙")
                else:
                    st.error(f"Error: {data.get('message', 'No se encontraron registros')}")

            except Exception as e:
                st.error(f"Error de conexión: {str(e)}")
        else:
            st.warning("El DNI debe tener 8 dígitos.")

if __name__ == "__main__":
    run()
