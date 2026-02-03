import streamlit as st
import requests

def run():
    st.markdown("<h1 style='text-align: center;'>🛡️ Consulta SOAT Inteligente</h1>", unsafe_allow_html=True)
    
    st.markdown("""
    ### 📝 Instrucciones:
    1. Presiona el botón **'1. Abrir Validador'** para resolver el captcha en la página oficial.
    2. Una vez resuelto (cuando veas los datos en esa página), regresa aquí.
    3. Ingresa la placa y presiona **'2. Sincronizar Reporte'**.
    """)

    col_buttons = st.columns(2)
    
    with col_buttons[0]:
        # Botón que abre la web oficial en otra pestaña
        st.link_button("1. 🌐 Abrir Validador", "https://www.interseguro.pe/soat/consulta-soat", use_container_width=True)

    with col_buttons[1]:
        placa = st.text_input("Placa a sincronizar", max_chars=6, placeholder="ABC123").upper()

    if st.button("2. 🔄 SINCRONIZAR REPORTE DETALLADO", use_container_width=True):
        if not placa:
            st.error("Por favor, ingresa la placa que validaste.")
            return

        with st.spinner("Sincronizando con el servidor de seguros..."):
            # Intentamos la extracción con headers que imitan la sesión activa
            url = f"https://www.interseguro.pe/soat/api/v1/soat/consultar-soat-vigente/{placa}"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0",
                "Referer": "https://www.interseguro.pe/soat/consulta-soat",
                "Accept": "application/json"
            }

            try:
                res = requests.get(url, headers=headers, timeout=10)
                
                if res.status_code == 200:
                    data = res.json()
                    if data.get("success"):
                        info = data.get("data")
                        st.balloons()
                        
                        # --- DISEÑO DEL REPORTE FINAL ---
                        st.markdown("---")
                        st.subheader(f"📊 Reporte Detallado: {placa}")
                        
                        with st.container(border=True):
                            c1, c2 = st.columns(2)
                            with c1:
                                st.write(f"**Aseguradora:** {info.get('companiaNombre')}")
                                st.write(f"**Estado:** :green[{info.get('estadoDescripcion')}]")
                                st.write(f"**Certificado:** {info.get('numeroCertificado')}")
                            with c2:
                                st.write(f"**Vencimiento:** {info.get('fechaFin')}")
                                st.write(f"**Uso:** {info.get('usoDescripcion')}")
                                st.write(f"**Clase:** {info.get('claseDescripcion')}")
                        
                        st.success("Información extraída correctamente.")
                    else:
                        st.warning("⚠️ No se pudo sincronizar. Asegúrate de haber resuelto el captcha en la otra pestaña.")
                else:
                    st.error(f"Error de conexión ({res.status_code}).")
            except Exception as e:
                st.error(f"Fallo en el puente: {str(e)}")

if __name__ == "__main__":
    run()
