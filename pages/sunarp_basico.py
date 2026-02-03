import streamlit as st
import requests

# 1. Estilos CSS para el efecto Hover y diseño de tarjetas
def local_css():
    st.markdown("""
        <style>
        /* Efecto de elevación y escala al pasar el mouse */
        .card-container {
            background-color: #ffffff;
            border-radius: 12px;
            padding: 20px;
            border: 1px solid #e1e8ed;
            transition: all 0.3s ease-in-out;
            cursor: pointer;
            margin-bottom: 15px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
        .card-container:hover {
            transform: scale(1.03); /* Se agranda sutilmente */
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
            border-color: #2e59d9;
        }
        .card-header-text {
            color: #2e59d9;
            font-weight: 700;
            font-size: 1.1rem;
            margin-bottom: 8px;
        }
        .badge-activa {
            background-color: #d4edda;
            color: #155724;
            padding: 3px 10px;
            border-radius: 50px;
            font-size: 0.75rem;
            font-weight: bold;
        }
        </style>
    """, unsafe_allow_html=True)

# 2. Función del Modal (Pop-up de detalles)
@st.dialog("DETALLES COMPLETOS")
def ver_detalle(item):
    st.markdown(f"### 📋 Partida: {item.get('numeroPartida')}")
    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("**👤 TITULAR:**")
        st.info(item.get('nombre'))
        st.write("**📍 ZONA:**")
        st.text(item.get('zona'))
    with col2:
        st.write("**🪪 DOCUMENTO:**")
        st.info(f"{item.get('Tipo Documento')}: {item.get('Núm. Documento')}")
        st.write("**🏢 OFICINA:**")
        st.text(item.get('oficina'))
    
    st.divider()
    st.write(f"**📖 REGISTRO:** {item.get('registro')}")
    st.write(f"**🚗 PLACA:** {item.get('Núm. Placa') or 'N/A'}")

def run():
    local_css()
    st.title("🚗 Consulta SUNARP Básico")
    
    # Mantenemos los resultados en memoria para que no se borren
    if 'data_sunarp' not in st.session_state:
        st.session_state.data_sunarp = None

    dni = st.text_input("Ingrese DNI para buscar", max_chars=8, placeholder="Ejm: 12345678")

    if st.button("🔍 BUSCAR REGISTROS"):
        API_URL = "https://seeker-v6.com/personas/sunarpbasicoapi"
        TOKEN = "sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"
        
        try:
            with st.spinner("Consultando..."):
                r = requests.post(API_URL, json={"dni": dni}, headers={"Authorization": f"Bearer {TOKEN}"})
                data = r.json()
                if data.get("status") == "success":
                    st.session_state.data_sunarp = data.get("data")
                else:
                    st.error(data.get("message"))
        except:
            st.error("Error de conexión con el servidor.")

    # Renderizado de Tarjetas
    if st.session_state.data_sunarp:
        st.markdown("---")
        # Mostramos en 3 columnas
        cols = st.columns(3)
        
        for idx, item in enumerate(st.session_state.data_sunarp):
            with cols[idx % 3]:
                # Tarjeta visual con Hover
                st.markdown(f"""
                    <div class="card-container">
                        <div class="card-header-text">{item.get('nombre')[:18]}...</div>
                        <p style="font-size: 0.85rem; color: #555;">
                            <b>Partida:</b> {item.get('numeroPartida')}<br>
                            <b>Oficina:</b> {item.get('oficina')}
                        </p>
                        <span class="badge-activa">● {item.get('estado')}</span>
                    </div>
                """, unsafe_allow_html=True)
                
                # Botón de Ver Detalles
                if st.button("Ver detalles completos →", key=f"btn_{idx}", use_container_width=True):
                    ver_detalle(item)

if __name__ == "__main__":
    run()
