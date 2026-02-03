import streamlit as st
import requests

def run():
    st.markdown("<h1 style='text-align: center;'>⚖️ Consulta de Denuncias</h1>", unsafe_allow_html=True)
    st.info("Búsqueda avanzada por DNI o Placa Vehicular")

    TOKEN = "sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"
    
    col1, col2 = st.columns([2, 1])
    with col1:
        search_value = st.text_input("Ingrese el dato a consultar", placeholder="DNI o Placa (ej: ABC123)")
    with col2:
        tipo_input = st.selectbox("Tipo de búsqueda", ["DNI", "PLACA"])

    if st.button("🔍 BUSCAR DENUNCIAS", use_container_width=True):
        if not search_value:
            st.warning("Por favor, ingrese un valor para buscar.")
            return

        # URL según documentación: método GET
        url = "https://seeker-v6.com/personas/apidenuncias"
        headers = {"Authorization": f"Bearer {TOKEN}"}
        params = {
            "searchValue": search_value,
            "tipo": tipo_input
        }

        with st.spinner("Consultando registros nacionales..."):
            try:
                # Al ser GET, usamos params en lugar de json
                res = requests.get(url, headers=headers, params=params, timeout=30)
                
                if res.status_code == 200:
                    data = res.json()
                    
                    if data.get("status") == "success":
                        st.success(f"✅ Búsqueda finalizada. Créditos restantes: {data.get('creditos_restantes')}")
                        
                        registros = data.get("data", [])
                        
                        if not registros:
                            st.info("No se encontraron denuncias registradas para este criterio.")
                        else:
                            # Mostramos cada denuncia en una tarjeta organizada
                            for idx, denuncia in enumerate(registros):
                                with st.container(border=True):
                                    st.subheader(f"📄 Registro #{idx + 1}")
                                    
                                    # Creamos columnas para los detalles
                                    c1, c2 = st.columns(2)
                                    # Adaptamos las llaves según lo que suele devolver Seeker en este módulo
                                    with c1:
                                        st.write(f"**Fecha:** {denuncia.get('fecha', 'N/A')}")
                                        st.write(f"**Delito:** {denuncia.get('delito', 'N/A')}")
                                    with c2:
                                        st.write(f"**Estado:** {denuncia.get('estado', 'N/A')}")
                                        st.write(f"**Entidad:** {denuncia.get('entidad', 'N/A')}")
                                    
                                    st.write(f"**Detalle:** {denuncia.get('detalle', 'No especificado')}")
                    else:
                        st.error(f"Error de la API: {data.get('message', 'Error desconocido')}")
                else:
                    st.error(f"Error de conexión (Código {res.status_code})")
            
            except Exception as e:
                st.error(f"Error inesperado: {str(e)}")

if __name__ == "__main__":
    run()
