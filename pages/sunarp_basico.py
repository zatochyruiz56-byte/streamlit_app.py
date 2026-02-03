import streamlit as st
import requests

# Configuración de estilo personalizada para el efecto "Hover" y tarjetas
def local_css():
    st.markdown("""
        <style>
        /* Efecto de agrandado en las tarjetas al pasar el mouse */
        .sunarp-card {
            background-color: white;
            border-radius: 10px;
            padding: 20px;
            border: 1px solid #e0e0e0;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            cursor: pointer;
            margin-bottom: 20px;
            min-height: 350px;
        }
        .sunarp-card:hover {
            transform: scale(1.05); /* Se agranda un poco */
            box-shadow: 0px 10px 20px rgba(0,0,0,0.1);
            border: 1px solid #2e59d9;
        }
        .card-header {
            background-color: #2e59d9;
            color: white;
            padding: 10px;
            border-radius: 8px 8px 0 0;
            margin: -20px -20px 15px -20px;
            font-size: 0.9rem;
            font-weight: bold;
        }
        .status-pill {
            background-color: #e8f5e9;
            color: #2e7d32;
            padding: 2px 8px;
            border-radius: 15px;
            font-size: 0.8rem;
            font-weight: bold;
        }
        </style>
    """, unsafe_allow_html=True)

# Ventana de detalles (Modal)
@st.dialog("Detalles de Partida SUNARP", width="large")
def mostrar_detalles_completos(item):
    st.write(f"🔢 **Número de Partida:** {item.get('numeroPartida')}")
    st.divider()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("**👤 Nombre Completo**")
        st.info(item.get('nombre'))
        st.write("**🏠 Dirección**")
        st.info(item.get('dirección') or "No especificada")
    with col2:
        st.write("**🪪 Documento**")
        st.info(item.get('Núm. Documento'))
        st.write("**✅ Estado**")
        st.success(item.get('estado'))
    with col3:
        st.write("**🚘 Placa**")
        st.info(item.get('Núm. Placa') or "N/A")
        st.write("**🏢 Oficina**")
        st.info(item.get('oficina'))

    st.warning("💡 **Información:** La consulta inicial trae los metadatos de la partida. Los documentos PDF se cargan bajo demanda.")

def run():
    local_css()
    st.title("🚗 Consulta SUNARP Básico")
    
    API_URL = "https://seeker-v6.com/personas/sunarpbasicoapi"
    TOKEN = "sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"
    
    dni = st.text_input("Número de DNI", max_chars=8, placeholder="48694322")

    if st.button("Buscar Registro 🔍"):
        payload = {"dni": dni}
        headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
        
        try:
            response = requests.post(API_URL, json=payload, headers=headers)
            data = response.json()

            if response.status_code == 200 and data.get("status") == "success":
                resultados = data.get("data", [])
                
                if not resultados:
                    st.info("No se encontraron registros.")
                    return

                st.subheader("Resultados de la Búsqueda")
                
                # Crear la cuadrícula de tarjetas (3 columnas)
                cols = st.columns(3)
                
                for idx, item in enumerate(resultados):
                    with cols[idx % 3]:
                        # Renderizamos la tarjeta visualmente con HTML/CSS
                        st.markdown(f"""
                            <div class="sunarp-card">
                                <div class="card-header">
                                    {item.get('nombre')[:25]}... <br>
                                    Partida: {item.get('numeroPartida')}
                                </div>
                                <p>🏢 <b>Oficina:</b><br>{item.get('oficina')}</p>
                                <p>📍 <b>Zona:</b><br>{item.get('zona')[:30]}...</p>
                                <p>📑 <b>Registro:</b><br>{item.get('registro')}</p>
                                <p><b>Estado:</b> <span class="status-pill">● {item.get('estado')}</span></p>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        # Botón real que activa el Modal
                        if st.button(f"Ver Detalles Completos →", key=f"btn_{idx}", use_container_width=True):
                            mostrar_detalles_completos(item)
            else:
                st.error("Error al consultar la API")
        except Exception as e:
            st.error(f"Fallo de conexión: {e}")

if __name__ == "__main__":
    run()
