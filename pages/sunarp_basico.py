import streamlit as st
import requests

def run():
    st.title("🚗 Consulta SUNARP Básico")
    
    API_URL = "https://seeker-v6.com/personas/sunarpbasicoapi"
    TOKEN = "sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"
    
    dni = st.text_input("Ingrese DNI para buscar propiedades", max_chars=8, placeholder="48694322")

    if st.button("🔍 BUSCAR REGISTROS"):
        headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
        payload = {"dni": dni}

        try:
            with st.spinner("Accediendo a Registros Públicos..."):
                response = requests.post(API_URL, json=payload, headers=headers)
                data = response.json()

            if response.status_code == 200 and data.get("status") == "success":
                resultados = data.get("data", [])
                
                if not resultados:
                    st.info("No se encontraron propiedades para este documento.")
                    return

                st.success(f"Se encontraron {len(resultados)} partidas registradas.")

                # --- DISEÑO DE PLANTILLA IDENTICA ---
                for idx, item in enumerate(resultados):
                    # Título de la partida con estilo de cabecera
                    st.markdown(f"### 📄 Detalles de Partida SUNARP: {item.get('numeroPartida')} — {item.get('oficina')}")
                    
                    # Contenedor principal
                    with st.container(border=True):
                        # Fila 1: Datos Personales
                        col1, col2, col3 = st.columns(3)
                        col1.write(f"👤 **Nombre Completo**\n\n{item.get('nombre')}")
                        col2.write(f"🪪 **Número de Documento**\n\n{item.get('Núm. Documento')}")
                        col3.write(f"🚘 **Número de Placa**\n\n{item.get('Núm. Placa') if item.get('Núm. Placa') else 'No especificado'}")
                        
                        st.divider()
                        
                        # Fila 2: Ubicación y Estado
                        col4, col5, col6 = st.columns(3)
                        col4.write(f"🏠 **Dirección**\n\n{item.get('dirección') if item.get('dirección') else 'No especificada'}")
                        estado = item.get('estado')
                        col5.write(f"✅ **Estado**\n\n{estado}")
                        col6.write(f"📖 **Libro de Registro**\n\n{item.get('libro')}")
                        
                        st.divider()

                        # Fila 3: Registro y Zona
                        col7, col8, col9 = st.columns(3)
                        col7.write(f"🗄️ **Tipo de Registro**\n\n{item.get('registro')}")
                        col8.write(f"🏢 **Oficina Registral**\n\n{item.get('oficina')}")
                        col9.write(f"📍 **Zona Registral**\n\n{item.get('zona')}")

                        # Botón decorativo de información (como en tu captura)
                        st.info(f"🔢 **Número de Partida:** {item.get('numeroPartida')}\n\nLa consulta inicial trae los metadatos de la partida (asientos, fechas, descripciones).")
                    
                    st.markdown("<br>", unsafe_allow_html=True) # Espacio entre tarjetas

                if "creditos_restantes" in data:
                    st.sidebar.metric("Saldo Actual", f"{data['creditos_restantes']} 🪙")

            else:
                st.error(f"Error: {data.get('message')}")

        except Exception as e:
            st.error(f"Error de conexión: {str(e)}")

if __name__ == "__main__":
    run()
