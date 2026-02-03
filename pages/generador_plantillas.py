import streamlit as st
import requests

def run():
    st.title("🗂️ Generador de Plantillas RENIEC")
    st.info("Este endpoint genera información detallada siguiendo un formato de plantilla específica.")

    # Configuración según imagen image_d4b2e4.png
    API_URL = "https://seeker-v6.com/personas/api/generadorplantillas"
    TOKEN = "sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"
    
    dni = st.text_input("Ingrese DNI de 8 dígitos", max_chars=8)
    # Según la documentación, el parámetro 'tipo' define la plantilla
    tipo_plantilla = st.selectbox("Seleccione tipo de plantilla", ["basica", "completa", "moderna"])

    if st.button("📄 GENERAR PLANTILLA"):
        if len(dni) == 8:
            headers = {
                "Authorization": f"Bearer {TOKEN}",
                "Content-Type": "application/json"
            }
            # Parámetros según documentación: dni, tipo
            payload = {
                "dni": dni,
                "tipo": tipo_plantilla
            }

            try:
                with st.spinner("Generando documento..."):
                    response = requests.post(API_URL, json=payload, headers=headers)
                    
                    # Verificación de respuesta JSON vs HTML (Login)
                    if "application/json" not in response.headers.get("Content-Type", ""):
                        st.error("❌ El servidor redirigió al Login. Este módulo podría estar restringido.")
                        return

                    data = response.json()

                if response.status_code == 200 and data.get("status") == "success":
                    st.success("✅ Plantilla generada correctamente")
                    
                    # --- VISTA DE PLANTILLA ---
                    st.markdown("### 📋 Ficha de Datos")
                    # El contenido suele venir dentro de data['data']
                    resultado = data.get("data", {})
                    
                    if isinstance(resultado, dict):
                        # Mostramos los datos en un formato de tabla o columnas
                        for clave, valor in resultado.items():
                            st.write(f"**{clave.replace('_', ' ').upper()}:** {valor}")
                    else:
                        st.write(resultado)
                    
                    if "creditos_restantes" in data:
                        st.sidebar.metric("Saldo", f"{data['creditos_restantes']} 🪙")
                else:
                    st.error(f"Error: {data.get('message', 'No se pudo generar la plantilla')}")

            except Exception as e:
                st.error(f"Error de conexión: {str(e)}")
        else:
            st.warning("Ingrese un DNI válido.")

if __name__ == "__main__":
    run()
