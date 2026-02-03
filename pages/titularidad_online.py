import streamlit as st
import requests
import json

def run():
    # Estilo básico para el contenedor
    st.markdown("""
        <style>
        .reportview-container .main .block-container {
            max-width: 900px;
        }
        .stCodeBlock {
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("📲 Titularidad Online (Raw Data)")
    st.info("Este módulo muestra la respuesta JSON exacta del servidor de Seeker-V6.")

    # Buscador
    dni = st.text_input("Número de DNI", max_chars=8, placeholder="Ejm: 12345678")

    if st.button("🚀 EJECUTAR CONSULTA API", use_container_width=True):
        if not dni:
            st.warning("Por favor, ingrese un DNI.")
            return

        API_URL = "https://seeker-v6.com/telefonos/titularidad"
        TOKEN = "sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"
        
        try:
            with st.spinner("Solicitando datos crudos..."):
                # Petición idéntica a tu ejemplo de requests
                response = requests.post(
                    API_URL, 
                    headers={"Authorization": f"Bearer {TOKEN}"}, 
                    json={"doc": dni}
                )
                
                # Verificamos si la respuesta es JSON
                if "application/json" in response.headers.get("Content-Type", ""):
                    raw_data = response.json()
                    
                    st.success("✅ Respuesta recibida correctamente")
                    
                    # --- MOSTRAR RESPUESTA CRUDA ---
                    st.markdown("### 📦 JSON Response")
                    st.code(json.dumps(raw_data, indent=4, ensure_ascii=False), language="json")
                    
                    # Opcional: Mostrar créditos si vienen en la respuesta
                    if "creditos_restantes" in raw_data:
                        st.sidebar.metric("Saldo", raw_data["creditos_restantes"])
                else:
                    st.error("❌ El servidor no respondió con un JSON válido.")
                    st.markdown("**Respuesta recibida:**")
                    st.code(response.text)

        except Exception as e:
            st.error(f"🔥 Error crítico: {str(e)}")

if __name__ == "__main__":
    run()
