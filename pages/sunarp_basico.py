import streamlit as st
import requests

# 1. CSS de Alta Fidelidad (Estética de Dashboard Premium)
def aplicar_estilos_premium():
    st.markdown("""
        <style>
        /* Tarjeta Principal */
        .card-premium {
            background: #ffffff;
            border-radius: 18px;
            padding: 25px;
            border: 1px solid #edf2f7;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            box-shadow: 0 4px 12px rgba(0,0,0,0.03);
            margin-bottom: 10px;
        }
        .card-premium:hover {
            transform: translateY(-10px);
            box-shadow: 0 20px 30px rgba(0,0,0,0.08);
            border-color: #3182ce;
        }
        .titular-header {
            color: #1a202c;
            font-size: 1rem;
            font-weight: 800;
            text-transform: uppercase;
            margin-bottom: 10px;
            line-height: 1.2;
        }
        .data-label {
            color: #718096;
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
            margin-top: 8px;
        }
        .badge-activa {
            background-color: #d1fae5;
            color: #065f46;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 0.7rem;
            font-weight: bold;
            display: inline-block;
            border: 1px solid #a7f3d0;
        }
        /* Estilo para los bloques de información en el Modal */
        .info-box {
            background-color: #f8fafc;
            padding: 16px;
            border-radius: 12px;
            border-left: 5px solid #3182ce;
            margin-bottom: 15px;
        }
        </style>
    """, unsafe_allow_html=True)

# 2. Modal de Detalles (Información completa sin redundancia)
@st.dialog("📋 DETALLES DE PARTIDA REGISTRAL", width="large")
def modal_detalle_completo(item):
    st.markdown(f"### Partida N° {item.get('numeroPartida')}")
    st.caption(f"Registro: {item.get('registro')}")
    st.divider()

    # BLOQUE 1: IDENTIDAD
    st.markdown("<div class='info-box'>", unsafe_allow_html=True)
    st.caption("TITULAR REGISTRADO")
    st.markdown(f"**{item.get('nombre')}**")
    st.markdown("</div>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.caption("DOCUMENTO")
        st.write(f"{item.get('Tipo Documento')}: {item.get('Núm. Documento')}")
    with c2:
        st.caption("PLACA")
        st.write(item.get('Núm. Placa') if item.get('Núm. Placa') else "N/A")
    with c3:
        st.caption("ESTADO")
        st.markdown(f"<span class='badge-activa'>● {item.get('estado')}</span>", unsafe_allow_html=True)

    st.divider()

    # BLOQUE 2: DATOS TÉCNICOS Y UBICACIÓN
    col_a, col_b = st.columns(2)
    with col_a:
        st.caption("DIRECCIÓN")
        st.write(item.get('dirección') if item.get('dirección') else "No registrada")
        st.caption("ZONA REGISTRAL")
        st.write(item.get('zona'))
        st.caption("LIBRO")
        st.write(item.get('libro'))
    with col_b:
        st.caption("OFICINA")
        st.write(item.get('oficina'))
        st.caption("ÁREA (HA)")
        st.write(item.get('area_ha') if item.get('area_ha') else "---")
        st.caption("UNIDAD CATASTRAL")
        st.write(item.get('unidad_catastral') if item.get('unidad_catastral') else "---")

    st.divider()
    if st.button("Cerrar Ficha", use_container_width=True):
        st.rerun()

def run():
    aplicar_estilos_premium()
    st.title("🚗 Buscador de Propiedades SUNARP")
    
    # Session state para mantener resultados
    if 'sunarp_data' not in st.session_state:
        st.session_state.sunarp_data = None

    # Buscador principal
    with st.container():
        dni = st.text_input("Número de DNI", max_chars=8, placeholder="Ejm: 12345678")
        if st.button("Consultar Registros 🔍", use_container_width=True):
            API_URL = "https://seeker-v6.com/personas/sunarpbasicoapi"
            TOKEN = "sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"
            
            try:
                with st.spinner("Buscando en registros públicos..."):
                    r = requests.post(API_URL, json={"dni": dni}, headers={"Authorization": f"Bearer {TOKEN}"})
                    data = r.json()
                    if data.get("status") == "success":
                        st.session_state.sunarp_data = data.get("data")
                    else:
                        st.error(f"Aviso: {data.get('message')}")
            except:
                st.error("Error de conexión.")

    # Renderizado de Tarjetas (Grid de 3 columnas)
    if st.session_state.sunarp_data:
        st.markdown("<br>", unsafe_allow_html=True)
        cols = st.columns(3)
        
        for idx, item in enumerate(st.session_state.sunarp_data):
            with cols[idx % 3]:
                st.markdown(f"""
                    <div class="card-premium">
                        <div class="titular-header">{item.get('nombre')[:22]}...</div>
                        <div class="data-label">PARTIDA</div>
                        <div style="font-weight: 700; color: #3182ce; font-size: 1.1rem;">{item.get('numeroPartida')}</div>
                        <div class="data-label">OFICINA</div>
                        <div style="font-size: 0.85rem; color: #4a5568;">{item.get('oficina')}</div>
                        <div style="margin-top: 15px;">
                            <span class="badge-activa">● {item.get('estado')}</span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                # Botón de acción transparente sobre la tarjeta
                if st.button("Ver detalles completos →", key=f"btn_{idx}", use_container_width=True):
                    modal_detalle_completo(item)

if __name__ == "__main__":
    run()
