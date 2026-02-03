import streamlit as st
import requests

# 1. CSS de Alta Fidelidad (Modern UI)
def aplicar_estilos_modernos():
    st.markdown("""
        <style>
        /* Tarjeta Principal con Efecto Hover Profundo */
        .card-moderna {
            background: white;
            border-radius: 16px;
            padding: 24px;
            border: 1px solid #f0f2f6;
            transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1);
            box-shadow: 0 4px 6px rgba(0,0,0,0.02);
            margin-bottom: 20px;
        }
        .card-moderna:hover {
            transform: translateY(-8px) scale(1.02);
            box-shadow: 0 20px 40px rgba(0,0,0,0.08);
            border-color: #4A90E2;
        }
        .titular-name {
            color: #1E293B;
            font-size: 1.1rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 12px;
        }
        .badge-status {
            background-color: #DCFCE7;
            color: #166534;
            padding: 4px 12px;
            border-radius: 99px;
            font-size: 0.75rem;
            font-weight: 700;
            border: 1px solid #BBF7D0;
        }
        /* Estilo para los labels en el Modal */
        .detail-label {
            color: #64748B;
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
            margin-bottom: 4px;
        }
        </style>
    """, unsafe_allow_html=True)

# 2. Modal Detallado (Toda la información de la API)
@st.dialog("📋 FICHA REGISTRAL COMPLETA", width="large")
def modal_full_info(item):
    aplicar_estilos_modernos() # Asegurar estilos dentro del iframe
    
    st.markdown(f"### Partida N° {item.get('numeroPartida')}")
    st.caption(f"Registro: {item.get('registro')}")
    
    st.divider()
    
    # Bloque 1: Identidad del Titular
    st.markdown("##### 👤 Datos del Titular")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.caption("NOMBRE COMPLETO")
        st.write(f"**{item.get('nombre')}**")
    with c2:
        st.caption("APELLIDO PATERNO")
        st.write(item.get('Ap. Paterno'))
    with c3:
        st.caption("APELLIDO MATERNO")
        st.write(item.get('Ap. Materno'))
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Bloque 2: Documentación y Placa
    c4, c5, c6 = st.columns(3)
    with c4:
        st.caption("TIPO DOC / NÚMERO")
        st.write(f"**{item.get('Tipo Documento')}:** {item.get('Núm. Documento')}")
    with c5:
        st.caption("NÚM. PLACA")
        st.write(f"**{item.get('Núm. Placa') if item.get('Núm. Placa') else 'SIN PLACA'}**")
    with c6:
        st.caption("ESTADO")
        st.markdown(f"<span class='badge-status'>{item.get('estado')}</span>", unsafe_allow_html=True)

    st.divider()

    # Bloque 3: Ubicación y Zona
    st.markdown("##### 📍 Ubicación y Registro")
    c7, c8 = st.columns(2)
    with c7:
        st.caption("DIRECCIÓN")
        st.write(item.get('dirección') if item.get('dirección') else "---")
        st.caption("ZONA REGISTRAL")
        st.write(item.get('zona'))
    with c8:
        st.caption("OFICINA")
        st.write(item.get('oficina'))
        st.caption("LIBRO")
        st.write(item.get('libro'))

    st.divider()

    # Bloque 4: Datos Técnicos (Área y Catastro)
    st.markdown("##### 🏗️ Información Técnica")
    c9, c10 = st.columns(2)
    with c9:
        st.caption("ÁREA (HA)")
        st.write(item.get('area_ha') if item.get('area_ha') else "No registrada")
    with col10 := c10:
        st.caption("UNIDAD CATASTRAL")
        st.write(item.get('unidad_catastral') if item.get('unidad_catastral') else "No registrada")

    if st.button("Cerrar Ficha", use_container_width=True):
        st.rerun()

def run():
    aplicar_estilos_modernos()
    st.title("🚗 Buscador de Propiedades SUNARP")
    
    if 'sunarp_results' not in st.session_state:
        st.session_state.sunarp_results = None

    # Campo de búsqueda moderno
    dni = st.text_input("Ingrese número de documento", max_chars=8, placeholder="Ejm: 12345678")

    if st.button("Realizar Búsqueda 🔍", use_container_width=True):
        API_URL = "https://seeker-v6.com/personas/sunarpbasicoapi"
        TOKEN = "sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"
        
        try:
            with st.spinner("Consultando Base de Datos..."):
                r = requests.post(API_URL, json={"dni": dni}, headers={"Authorization": f"Bearer {TOKEN}"})
                data = r.json()
                if data.get("status") == "success":
                    st.session_state.sunarp_results = data.get("data")
                else:
                    st.error(f"Aviso: {data.get('message')}")
        except:
            st.error("Error de comunicación.")

    # Renderizado de la Cuadrícula
    if st.session_state.sunarp_results:
        st.markdown("<br>", unsafe_allow_html=True)
        cols = st.columns(3)
        
        for idx, item in enumerate(st.session_state.sunarp_results):
            with cols[idx % 3]:
                # Tarjeta visual con la info clave y efecto Hover
                st.markdown(f"""
                    <div class="card-moderna">
                        <div class="titular-name">{item.get('nombre')[:22]}...</div>
                        <p style="font-size: 0.8rem; color: #64748B; margin-bottom: 5px;">
                            <b>PARTIDA:</b> {item.get('numeroPartida')}<br>
                            <b>OFICINA:</b> {item.get('oficina')}
                        </p>
                        <span class="badge-status">{item.get('estado')}</span>
                    </div>
                """, unsafe_allow_html=True)
                
                # Botón de acción integrado
                if st.button("Ver detalles completos →", key=f"btn_{idx}", use_container_width=True):
                    modal_full_info(item)

if __name__ == "__main__":
    run()
