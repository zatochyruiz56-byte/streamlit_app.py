import streamlit as st
import requests

def run():
    st.markdown("<h1 style='text-align: center;'>🛡️ Consulta de SOAT</h1>", unsafe_allow_html=True)

    TOKEN = "sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"
    placa_input = st.text_input("Ingrese Placa para SOAT", max_chars=7, placeholder="ABC123").upper()

    if st.button("🚀 VERIFICAR SOAT", use_container_width=True):
        if not placa_input:
            st.warning("Por favor, ingrese una placa.")
            return

        # Endpoint según documentación (Método GET)
        url = "https://seeker-v6.com/vehiculos/soat_vehicular"
        headers = {"Authorization": f"Bearer {TOKEN}"}
        params = {"placa": placa_input}

        with st.spinner("Consultando vigencia de seguros..."):
            try:
                # Al ser GET, usamos params
                res = requests.get(url, headers=headers, params=params, timeout=20)
                
                # Verificación de error de sesión (Login HTML)
                if "text/html" in res.headers.get("Content-Type", ""):
                    st.error("🚨 Error Crítico: El servicio SOAT también redirige al Login.")
                    with st.expander("Ver diagnóstico del servidor"):
                        st.code(res.text[:500])
                    return

                data = res.json()

                if data.get("status") == "success":
                    st.success(f"✅ Consulta procesada. Créditos restantes: {data.get('creditos_restantes')}")
                    
                    soat = data.get("data", {})
                    if soat:
                        st.subheader("📄 Información del Seguro")
                        
                        # Mostramos los campos típicos del SOAT
                        c1, c2 = st.columns(2)
                        with c1:
                            st.write(f"**Compañía:** {soat.get('compania', 'N/A')}")
                            st.write(f"**Estado:** {soat.get('estado', 'N/A')}")
                        with c2:
                            st.write(f"**Inicio:** {soat.get('fecha_inicio', 'N/A')}")
                            st.write(f"**Fin:** {soat.get('fecha_fin', 'N/A')}")
                        
                        st.write(f"**Uso del Vehículo:** {soat.get('uso', 'N/A')}")
                    else:
                        st.info("No se encontró información de SOAT para esta placa.")
                else:
                    st.error(f"Error: {data.get('message', 'Servicio no disponible')}")

            except Exception as e:
                st.error(f"Error de conexión: {str(e)}")

if __name__ == "__main__":
    run()
