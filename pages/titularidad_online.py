import streamlit as st
import requests
import json

def run():
    # Estilos para una interfaz de investigación
    st.markdown("""
        <style>
        .stCodeBlock {
            background-color: #050505 !important;
            border: 1px solid #1e1e1e !important;
            border-radius: 10px !important;
        }
        .status-box {
            padding: 10px;
            border-radius: 8px;
            font-weight: bold;
            text-align: center;
            margin-bottom: 20px;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("📞 Consulta Osiptel Database")
    st.info("Búsqueda de titularidad mediante número celular (Base de Datos Osiptel).")

    # Parámetros técnicos
    API_URL = "https://seeker-v6.com/telefonos/consulta_osiptel_database_tel"
    TOKEN = "sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"

    # Input específico para Teléfono
    telefono = st.text_input("Ingrese número de celular", max_chars=9, placeholder="Ejm: 987654321")

    if st.button("🚀 CONSULTAR TITULARIDAD", use_container_width=True):
        if not telefono or len(telefono) < 9:
            st.warning("⚠️ Ingrese un número de celular válido (9 dígitos).")
            return

        headers = {
            "Authorization": f"Bearer {TOKEN}",
            "Content-Type": "application/json"
        }
        
        # Payload según tu documentación: {"tel": "valor"}
        payload = {"tel": telefono}

        try:
            with st.spinner("Consultando base de datos Osiptel..."):
                response = requests.post(API_URL, json=payload, headers=headers, timeout=15)
            
            # Análisis de conexión
            if response.status_code == 200:
                st.markdown("<div style='background-color: #155724; color: white;' class='status-box'>CONEXIÓN EXITOSA (200 OK)</div>", unsafe_allow_html=True)
                
                # Intentamos procesar la data
                try:
                    data = response.json()
                    st.markdown("### 📦 Respuesta Cruda (JSON)")
                    st.code(json.dumps(data, indent=4, ensure_ascii=False), language="json")
                    
                    # Si la data trae resultados, los organizamos visualmente
                    if data.get("status") == "success" and "data" in data:
                        st.success("Titular encontrado.")
                        # Aquí podrías mapear los campos si ya supiéramos cómo los envía
                    
                except Exception:
                    st.error("❌ El servidor respondió, pero no envió un JSON válido.")
                    st.code(response.text, language="html")
            
            elif response.status_code == 401 or response.status_code == 403:
                st.error("🚫 Error de Autorización: Tu token no tiene acceso a este módulo.")
            else:
                st.error(f"⚠️ Servidor Caído o Inestable: Código {response.status_code}")
                with st.expander("Ver detalle del error"):
                    st.code(response.text)

        except Exception as e:
            st.error(f"🔥 No se pudo establecer conexión: {str(e)}")

if __name__ == "__main__":
    run()
