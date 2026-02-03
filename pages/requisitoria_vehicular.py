import streamlit as st
import requests
import json

def run():
    st.title("🚓 Requisitorias Vehiculares")
    st.info("Consulta de órdenes de captura y requisitorias para vehículos por placa.")

    # Configuración técnica
    API_URL = "https://seeker-v6.com/personas/requisitorias_vehiculares"
    TOKEN = "sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"

    # Layout de búsqueda
    col_input, col_ver = st.columns([2, 1])
    
    with col_input:
        placa = st.text_input("Número de Placa", max_chars=7, placeholder="Ejm: ABC-123")
    with col_ver:
        version = st.selectbox("Versión de API", ["v1", "v2"])

    if st.button("🔍 CONSULTAR REQUISITORIA", use_container_width=True):
        if not placa:
            st.warning("⚠️ Ingrese una placa para continuar.")
            return

        headers = {
            "Authorization": f"Bearer {TOKEN}",
            "Content-Type": "application/json"
        }
        
        # Payload exacto según tu ejemplo
        payload = {
            "placa": placa.replace("-", "").upper(), # Limpiamos el guion por si acaso
            "version": version
        }

        try:
            with st.spinner("Conectando con el registro policial..."):
                response = requests.post(API_URL, json=payload, headers=headers, timeout=20)
            
            # --- ZONA DE RESULTADOS ---
            if response.status_code == 200:
                try:
                    data = response.json()
                    
                    # Mostramos la respuesta cruda primero para ver qué campos trae
                    st.markdown("### 📦 Respuesta Cruda del Servidor")
                    st.code(json.dumps(data, indent=4, ensure_ascii=False), language="json")

                    # Si la respuesta es exitosa, creamos una ficha visual rápida
                    if data.get("status") == "success":
                        st.success("✅ Consulta realizada con éxito.")
                        
                        # Aquí diseñamos la ficha visual según lo que retorne la API
                        res = data.get("data", {})
                        if res:
                            with st.container(border=True):
                                st.subheader(f"🚘 Resultado Placa: {placa.upper()}")
                                c1, c2 = st.columns(2)
                                # Ejemplo de mapeo (ajustar según lo que veas en el JSON crudo)
                                c1.write(f"**Estado:** {res.get('estado', 'SIN REQUISITORIA')}")
                                c2.write(f"**Motivo:** {res.get('motivo', 'Ninguno')}")
                        else:
                            st.info("El vehículo no presenta requisitorias registradas.")
                    else:
                        st.error(f"Error de API: {data.get('message', 'Error desconocido')}")

                except Exception:
                    st.error("❌ El servidor respondió, pero no envió JSON.")
                    st.code(response.text)
            else:
                st.error(f"⚠️ Error {response.status_code}: El servidor no pudo procesar la solicitud.")
                st.code(response.text)

        except Exception as e:
            st.error(f"🔥 Error de conexión: {str(e)}")

if __name__ == "__main__":
    run()
