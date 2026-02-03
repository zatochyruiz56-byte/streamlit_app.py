import streamlit as st
import requests

# 1. Configuración de Estilos (CSS) para el efecto Hover y Tarjetas
def aplicar_estilos():
    st.markdown("""
        <style>
        /* Contenedor de la cuadrícula */
        .main-container {
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            justify-content: center;
        }
        /* La Tarjeta Visual */
        .sunarp-card {
            background-color: #ffffff;
            border-radius: 15px;
            padding: 20px;
            border: 1px solid #e0e6ed;
            transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
            text-align: left;
            height: 100%;
        }
        /* Efecto de agrandado y sombra al pasar el mouse */
        .sunarp-card:hover {
            transform: translateY(-5px) scale(1.02);
            box-shadow: 0 15px 30px rgba(0,0,0,0.1);
            border-color: #3498db;
        }
        .card-title {
            color: #1a202c;
            font-size: 1.1rem;
            font-weight: 700;
            margin-bottom: 10px;
            border-bottom: 2px solid #3498db;
            padding-bottom: 5px;
        }
        .status-badge {
            background-color: #d1fae5;
            color: #065f46;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 600;
            display: inline-block;
            margin-top: 10px;
        }
        /* Estilo para el botón de Streamlit dentro de la tarjeta */
        div.stButton > button {
            border-radius: 8px;
            font-weight: 600;
            transition: all 0.2s;
        }
        </style>
    """, unsafe_allow_html=True)

# 2. Plantilla de Detalles (El Modal que se abre)
@st.dialog("📋 DETALLES COMPLETOS DE LA PARTIDA", width="large")
def modal_detalles(item):
    st.markdown(f"### Partida N° {item.get('numeroPartida')}")
    st.divider()
    
    # Diseño de Ficha Identidad (Igual a tu captura)
    c1, c2 = st.columns(2)
    with c1:
        st.write("👤 **NOMBRE DEL TITULAR**")
        st.code(item.get('nombre'), language="text")
        st.write("📍 **ZONA REGISTRAL**")
        st.code(item.get('zona'), language="text")
    with c2:
        st.write("🪪 **DOCUMENTO**")
        st.code(f"{item.get('Tipo Documento')}: {item.get('Núm. Documento')}", language="text")
        st.write("🏢 **OFICINA**")
        st.code(item.get('oficina'), language="text")
    
    st.divider()
    
    c3, c4, c5 = st.columns(3)
    c3.metric("ESTADO", item.get('estado'))
    c4.metric("LIBRO", "PREDIOS" if "PREDIOS" in item.get('libro') else "VEHICULAR")
    c5.metric("PLACA", item.get('Núm. Placa') or "N/A")

    if st.button("Cerrar Detalle"):
        st.rerun()

def run():
    aplicar_estilos()
    st.title("🚗 Sistema de Consultas SUNARP")
    
    # Inicializar el estado de búsqueda para que no se borre al hacer clic
    if 'resultados_sunarp' not in st.session_state:
        st.session_state.resultados_sunarp = None

    with st.container():
        dni = st.text_input("Ingrese DNI para buscar", max_chars=8)
        btn_buscar = st.button("Consultar Registros 🔍", use_container_width=True)

    if btn_buscar and dni:
        API_URL = "https://seeker-v6.com/personas/sunarpbasicoapi"
        TOKEN = "sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"
        
        try:
            with st.spinner("Conectando con SUNARP..."):
                r = requests.post(API_URL, json={"dni": dni}, headers={"Authorization": f"Bearer {TOKEN}"})
                data = r.json()
                if data.get("status") == "success":
                    st.session_state.resultados_sunarp = data.get("data", [])
                else:
                    st.error(data.get("message"))
        except:
            st.error("Error de conexión.")

    # Si hay resultados guardados, dibujamos las tarjetas
    if st.session_state.resultados_sunarp:
        st.markdown("---")
        cols = st.columns(3) # Cuadrícula de 3
        
        for idx, item in enumerate(st.session_state.resultados_sunarp):
            with cols[idx % 3]:
                # Tarjeta Visual con efecto Hover
                st.markdown(f"""
                    <div class="sunarp-card">
                        <div class="card-title">{item.get('nombre')[:20]}...</div>
                        <p style='font-size: 0.85rem; color: #666;'>
                            <b>Partida:</b> {item.get('numeroPartida')}<br>
                            <b>Oficina:</b> {item.get('oficina')}<br>
                            <b>Registro:</b> {item.get('registro')[:25]}...
                        </p>
                        <span class="status-badge">● {item.get('estado')}</span>
                    </div>
                """, unsafe_allow_html=True)
                
                # Botón de acción
                if st.button("Ver detalles completos", key=f"det_{idx}", use_container_width=True):
                    modal_detalles(item)

if __name__ == "__main__":
    run()
