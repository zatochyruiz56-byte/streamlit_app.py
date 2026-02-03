import streamlit as st
import requests
import json

def run():
    # Estilos para una terminal de datos moderna
    st.markdown("""
        <style>
        .stCodeBlock {
            background-color: #0e1117 !important;
            border: 1px solid #30363d !important;
            border-radius: 12px !important;
        }
        .json-label {
            background-color: #1f2937;
            color: #60a5fa;
            padding: 5px 12px;
            border-radius: 8px;
            font-size: 0.8rem;
            font-weight: bold;
            display: inline-block;
            margin-bottom: 10px;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("📲 Titularidad Online (API Raw)")
    st.markdown("---")

    # Contenedor de búsqueda
    with st.container():
        dni = st.text_input("Ingrese DNI", max_chars=8, placeholder="Ejm: 12345678")
        
        if st.button("🚀 OBTENER JSON DE API", use_container_width=True):
            if len(dni) != 8:
                st.warning("⚠️ Formato de DNI inválido.")
                return

            API_URL = "https://seeker-v6.com/telefonos/titularidad"
            TOKEN = "sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"
            
            try:
                with st.spinner("Solicitando respuesta cruda al servidor..."):
                    # Petición según tu estructura
                    response = requests.post(
                        API_URL, 
                        headers={"Authorization": f"Bearer {TOKEN}"}, 
                        json={"doc": dni}
                    )
                    
                    # Verificación de respuesta
                    if response.status_code == 200:
                        try:
                            raw_json = response.json()
                            
                            st.markdown("<div class='json-label'>{ } JSON RESPONSE</div>", unsafe_allow_html=True)
                            
                            # Mostramos la data cruda formateada
                            st.code(json.dumps(raw_json, indent=4, ensure_ascii=False), language="json")
                            
                            # Mostrar estado de créditos si existe en la raíz del JSON
                            if "creditos_restantes" in raw_json:
                                st.sidebar.metric("Saldo actual", raw_json["creditos_restantes"])
                                
                        except ValueError:
                            st.error("❌ El servidor no respondió con un JSON válido.")
                            st.code(response.text, language="html")
                    else:
                        st.error(f"❌ Error del Servidor: Código {response.status_code}")
                        st.code(response.text)

            except Exception as e:
                st.error(f"🔥 Error de conexión: {str(e)}")

if __name__ == "__main__":
    run()
