import streamlit as st
import requests

# 1. CSS Premium para Tarjetas de Operadoras
def aplicar_estilos_telefonia():
    st.markdown("""
        <style>
        .phone-card {
            background: #ffffff;
            border-radius: 15px;
            padding: 20px;
            border-left: 5px solid #3498db;
            box-shadow: 0 4px 6px rgba(0,0,0,0.02);
            transition: all 0.3s ease;
            margin-bottom: 15px;
        }
        .phone-card:hover {
            transform: scale(1.02);
            box-shadow: 0 10px 20px rgba(0,0,0,0.05);
        }
        .operator-label {
            font-size: 0.75rem;
            font-weight: 800;
            text-transform: uppercase;
            color: #718096;
            margin-bottom: 5px;
        }
        .phone-number {
            font-size: 1.2rem;
            font-weight: 700;
            color: #2d3748;
        }
        .badge-online {
            background-color: #ebf8ff;
            color: #2b6cb0;
            padding: 2px 10px;
            border-radius: 10px;
            font-size: 0.7rem;
            font-weight: bold;
        }
        </style>
    """, unsafe_allow_html=True)

# 2. Modal de Detalles (Toda la información del Titular)
@st.dialog("📋 REPORTE DE TITULARIDAD", width="large")
def modal_titularidad(data):
    st.markdown(f"### Propietario: {data.get('nombre', 'No disponible')}")
    st.divider()
    
    # Grid de información
    c1, c2 = st.columns(2)
    with c1:
        st.caption("DOCUMENTO")
        st.write(f"**DNI:** {data.get('dni', '---')}")
    with c2:
        st.caption("TOTAL LÍNEAS")
        st.write(f"**{len(data.get('telefonos', []))} Líneas encontradas**")

    st.divider()
    
    # Listado de teléfonos detallado
    st.markdown("##### 📱 Desglose de Operadoras")
    telefonos = data.get('telefonos', [])
    if telefonos:
        for t in telefonos:
            col_op, col_num = st.columns([1, 2])
            col_op.info(f"**{t.get('operador', 'OTRO')}**")
            col_num.success(f"📞 {t.get('numero', '---')}")
    else:
        st.warning("No se encontraron números activos asociados.")

    if st.button("Cerrar Reporte", use_container_width=True):
        st.rerun()

def run():
    aplicar_estilos_telefonia()
    st.title("📲 Titularidad Online")
    
    if 'tel_results' not in st.session_state:
        st.session_state.tel_results = None

    # Buscador
    dni = st.text_input("Número de DNI para Titularidad", max_chars=8, placeholder="Ejm: 12345678")

    if st.button("Consultar Operadoras 🔍", use_container_width=True):
        API_URL = "https://seeker-v6.com/telefonos/titularidad"
        TOKEN = "sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"
        
        try:
            with st.spinner("Escaneando bases de datos telefónicas..."):
                # Parámetro 'doc' según tu código de ejemplo
                r = requests.post(API_URL, json={"doc": dni}, headers={"Authorization": f"Bearer {TOKEN}"})
                data = r.json()
                
                if data.get("status") == "success":
                    st.session_state.tel_results = data.get("data")
                else:
                    st.error(f"Aviso: {data.get('message', 'Error en consulta')}")
        except:
            st.error("Error de conexión con el servicio de telefonía.")

    # Renderizado de Tarjetas
    if st.session_state.tel_results:
        res = st.session_state.tel_results
        st.markdown(f"##### Resultado para: {res.get('nombre')}")
        
        # Grid de 3 columnas para los teléfonos
        telefonos = res.get('telefonos', [])
        cols = st.columns(3)
        
        for idx, t in enumerate(telefonos):
            with cols[idx % 3]:
                st.markdown(f"""
                    <div class="phone-card">
                        <div class="operator-label">{t.get('operador')}</div>
                        <div class="phone-number"># {t.get('numero')}</div>
                        <div class="badge-online">ACTIVA</div>
                    </div>
                """, unsafe_allow_html=True)

        if st.button("Ver reporte completo de titularidad →", use_container_width=True):
            modal_titularidad(res)

if __name__ == "__main__":
    run()
