import streamlit as st
import requests

# 1. CSS de Alta Fidelidad (UI Moderna con Efectos de Transición)
def aplicar_estilos_premium():
    st.markdown("""
        <style>
        /* Contenedor de la Tarjeta */
        .card-premium {
            background: #ffffff;
            border-radius: 18px;
            padding: 25px;
            border: 1px solid #edf2f7;
            transition: all 0.4s ease;
            box-shadow: 0 4px 12px rgba(0,0,0,0.03);
            margin-bottom: 10px;
        }
        /* Efecto Hover: Elevación y Borde Azul */
        .card-premium:hover {
            transform: translateY(-10px);
            box-shadow: 0 20px 30px rgba(0,0,0,0.08);
            border-color: #3182ce;
        }
        .titular-header {
            color: #2d3748;
            font-size: 1rem;
            font-weight: 800;
            text-transform: uppercase;
            margin-bottom: 10px;
            line-height: 1.2;
        }
        .data-label {
            color: #718096;
            font-size: 0.75rem;
            font-weight: 600;
            margin-top: 8px;
        }
        .badge-activa {
            background-color: #c6f6d5;
            color: #22543d;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 0.7rem;
            font-weight: bold;
            display: inline-block;
        }
        /* Estilo para los bloques de información en el Modal */
        .info-box {
            background-color: #f7fafc;
            padding: 15px;
            border-radius: 10px;
            border-left: 4px solid #3182ce;
            margin-bottom: 10px;
        }
        </style>
    """, unsafe_allow_html=True)

# 2. Modal Detallado (Visualización de toda la data de la API)
@st.dialog("📄 FICHA TÉCNICA REGISTRAL", width="large")
def modal_detalle_completo(item):
    st.markdown(f"### Partida N° {item.get('numeroPartida')}")
    st.write(f"**{item.get('registro')}**")
    st.divider()

    # SECCIÓN 1: DATOS DEL TITULAR
    st.markdown("#### 👤 Información del Titular")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"<div class='info-box'><b>Nombre Completo:</b><br>{item.get('nombre')}</div>", unsafe_allow_html=True)
        st.write(f"**Apellido Paterno:** {item.get('Ap. Paterno')}")
        st.write(f"**Apellido Materno:** {item.get('Ap. Materno')}")
    with col2:
        st.markdown(f"<div class='info-box'><b>Documento:</b><br>{item.get('Tipo Documento')} - {item.get('Núm. Documento')}</div>", unsafe_allow_html=True)
        st.write(f"**Estado de Partida:** {item.get('estado')}")

    st.divider()

    # SECCIÓN 2: DATOS DEL BIEN (VEHÍCULO / PREDIO)
    st.markdown("#### 🚗 / 🏠 Detalles del Bien")
    col3, col4 = st.columns(2)
    with col3:
        st.write(f"**Placa:** {item.get('Núm. Placa') if item.get('Núm. Placa') else 'N/A'}")
        st.write(f"**Dirección:** {item.get('dirección') if item.get('dirección') else 'No registrada'}")
        st.write(f"**Unidad Catastral:** {item.get('unidad_catastral') if item.get('unidad_catastral') else 'No registrada'}")
    with col4:
        st.write(f"**Área (HA):** {item.get('area_ha') if item.get('area_ha') else 'No registrada'}")
        st.write(f"**Libro:** {item.get('libro')}")

    st.divider()

    # SECCIÓN 3: REGISTRO Y UBICACIÓN
    st.markdown("#### 📍 Ubicación Administrativa")
    col5, col6 = st.columns(2)
    with col5:
        st.write(f"**Zona Registral:** {item.get('zona')}")
    with col6:
        st.write(f"**Oficina:** {item.get('oficina')}")

    if st.button("Cerrar Detalle", use_container_width=True):
        st.rerun()

def run():
    aplicar_estilos_premium()
    st.title("🚗 Consulta de Propiedades SUNARP")
    
    # Session state para persistencia
    if 'sunarp_data' not in st.session_state:
        st.session_state.sunarp_data = None

    # Buscador moderno
    with st.container():
        dni = st.text_input("Ingrese DNI", max_chars=8, placeholder="Ejm: 12345678")
        if st.button("Consultar Registros 🔍", use_container_width=True):
            API_URL = "https://seeker-v6.com/personas/sunarpbasicoapi"
            TOKEN = "sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"
            
            try:
                with st.spinner("Accediendo a la base de datos..."):
                    r = requests.post(API_URL, json={"dni": dni}, headers={"Authorization": f"Bearer {TOKEN}"})
                    data = r.json()
                    if data.get("status") == "success":
                        st.session_state.sunarp_data = data.get("data")
                    else:
                        st.error(f"Aviso: {data.get('message')}")
            except:
                st.error("Error de red.")

    # Renderizado de Tarjetas con Hover
    if st.session_state.sunarp_data:
        st.markdown("<br>", unsafe_allow_html=True)
        cols = st.columns(3)
        
        for idx, item in enumerate(st.session_state.sunarp_data):
            with cols[idx % 3]:
                # Tarjeta con estilos modernos
                st.markdown(f"""
                    <div class="card-premium">
                        <div class="titular-header">{item.get('nombre')[:20]}...</div>
                        <div class="data-label">PARTIDA</div>
                        <div style="font-weight: 700; color: #3182ce;">{item.get('numeroPartida')}</div>
                        <div class="data-label">OFICINA</div>
                        <div style="font-size: 0.85rem; color: #4a5568;">{item.get('oficina')}</div>
                        <div style="margin-top: 15px;">
                            <span class="badge-activa">● {item.get('estado')}</span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                # Botón de acción
                if st.button("Ver detalles completos →", key=f"btn_{idx}", use_container_width=True):
                    modal_detalle_completo(item)

if __name__ == "__main__":
    run()
