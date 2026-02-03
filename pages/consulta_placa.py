import streamlit as st
import requests

def run():
    st.markdown("<h1 style='text-align: center;'>🚗 Consulta de Placa Vehicular</h1>", unsafe_allow_html=True)

    TOKEN = "sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"
    placa_input = st.text_input("Ingrese Placa", max_chars=7, placeholder="ABC123").upper()

    if st.button("🔍 CONSULTAR DATOS DE PLACA", use_container_width=True):
        if not placa_input:
            st.warning("Por favor, ingrese una placa.")
            return

        # Endpoint según documentación oficial
        url = "https://seeker-v6.com/vehiculos/api_newPlacas"
        headers = {"Authorization": f"Bearer {TOKEN}"}
        payload = {"placa": placa_input}

        with st.spinner("Buscando información detallada del vehículo..."):
            try:
                res = requests.post(url, headers=headers, json=payload, timeout=30)
                
                # Verificación de error de sesión (redirección a HTML)
                if "text/html" in res.headers.get("Content-Type", ""):
                    st.error("❌ El servicio de Placas no está disponible (Error de Sesión en Seeker).")
                    with st.expander("Ver respuesta técnica"):
                        st.code(res.text[:500])
                    return

                data = res.json()

                if data.get("status") == "success":
                    st.success(f"✅ Datos recuperados. Créditos restantes: {data.get('creditos_restantes')}")
                    
                    vehiculo = data.get("data", {})
                    
                    # Organización de datos por secciones
                    col1, col2 = st.columns(2)
                    with col1:
                        st.subheader("📋 Datos Generales")
                        st.write(f"**Marca:** {vehiculo.get('marca', 'N/A')}")
                        st.write(f"**Modelo:** {vehiculo.get('modelo', 'N/A')}")
                        st.write(f"**Año:** {vehiculo.get('anho_modelo', 'N/A')}")
                        st.write(f"**Color:** {vehiculo.get('color', 'N/A')}")
                    
                    with col2:
                        st.subheader("⚙️ Detalles Técnicos")
                        st.write(f"**Serie/Chasis:** {vehiculo.get('serie', 'N/A')}")
                        st.write(f"**Motor:** {vehiculo.get('motor', 'N/A')}")
                        st.write(f"**Placa Vigente:** {vehiculo.get('placa_vigente', 'N/A')}")
                        st.write(f"**Estado:** {vehiculo.get('estado', 'N/A')}")

                    st.markdown("---")
                    st.subheader("👤 Información del Propietario")
                    st.write(f"**Nombre/Razón Social:** {vehiculo.get('propietario', 'No disponible')}")
                
                else:
                    st.error(f"Error de la API: {data.get('message', 'No se encontró la placa')}")

            except Exception as e:
                st.error(f"Fallo al conectar con el servidor: {str(e)}")

if __name__ == "__main__":
    run()
