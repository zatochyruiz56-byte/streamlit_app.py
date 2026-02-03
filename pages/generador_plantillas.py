import streamlit as st
import requests
import json

def run():
    st.title("🛠️ Diagnóstico de Errores - Seeker-V6")
    st.write("Usa este módulo para ver por qué la API no responde correctamente.")

    # Configuración de los parámetros según tu documentación
    API_URL = "https://seeker-v6.com/personas/api/generadorplantillas"
    TOKEN = "sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"
    
    dni = st.text_input("DNI a consultar", max_chars=8, value="45106211")
    tipo = st.selectbox("Tipo de plantilla", ["completa", "basica", "moderna"])

    if st.button("🔍 EJECUTAR Y VER ERROR REAL"):
        headers = {
            "Authorization": f"Bearer {TOKEN}",
            "Content-Type": "application/json"
        }
        payload = {
            "dni": dni,
            "tipo": tipo
        }

        try:
            with st.spinner("Consultando..."):
                # Realizamos la petición
                response = requests.post(API_URL, json=payload, headers=headers)
            
            # --- SECCIÓN DE DIAGNÓSTICO ---
            st.markdown("### 🛰️ Respuesta del Servidor")
            
            # 1. Mostrar Código de Estado (200=OK, 401=Token, 403=Saldo, 500=Error Servidor)
            if response.status_code == 200:
                st.success(f"Código de Estado: {response.status_code} (OK)")
            else:
                st.error(f"Código de Estado: {response.status_code}")

            # 2. Mostrar Headers (Útil para ver si es HTML o JSON)
            with st.expander("Ver Headers de respuesta"):
                st.write(dict(response.headers))

            # 3. Mostrar el Cuerpo de la Respuesta
            st.markdown("#### Contenido de la Respuesta:")
            
            content_type = response.headers.get("Content-Type", "")
            
            if "application/json" in content_type:
                # Si es JSON, lo mostramos bonito
                st.json(response.json())
            else:
                # Si NO es JSON (como en el error de Licencias), mostramos el texto crudo
                st.warning("⚠️ El servidor no envió un JSON. Posible redirección o error de servidor.")
                st.code(response.text, language="html")

        except Exception as e:
            st.error(f"🔥 Error crítico en el código Python: {str(e)}")

if __name__ == "__main__":
    run()
