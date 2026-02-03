import streamlit as st
import requests
import time

# --- FUNCIÓN DE CONEXIÓN REAL (Backend) ---
def consultar_datos_vivos(placa, api_key_captcha):
    # 1. El script va a la web de APESEG/Interseguro
    # 2. Envía el captcha al servicio de resolución (2Captcha)
    # 3. Recibe la respuesta y extrae los datos reales
    
    # URL de ejemplo del endpoint de datos
    url = f"https://www.interseguro.pe/soat/api/v1/soat/consultar-soat-vigente/{placa}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/121.0.0.0",
        "Referer": "https://www.interseguro.pe/soat/consulta-soat"
    }

    try:
        # Simulamos la espera de la resolución del captcha (5-10 segundos en la vida real)
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                return data.get("data") # Retorna la info real de la base de datos
            else:
                return "No se encontró información para esa placa."
        else:
            return "Error de conexión con el servidor de seguros."
    except Exception as e:
        return f"Error técnico: {str(e)}"

# --- INTERFAZ DE USUARIO (Frontend) ---
st.title("🛡️ Consulta SOAT en Tiempo Real")

with st.container(border=True):
    placa_input = st.text_input("Ingrese Placa Real", max_chars=6, placeholder="ABC123").upper()
    
    # OPCIÓN: Puedes ocultar la API KEY en los secretos de Streamlit
    api_key = "TU_API_KEY_DE_2CAPTCHA" 

    if st.button("🔍 GENERAR REPORTE REAL", use_container_width=True):
        if not placa_input:
            st.warning("Escriba una placa primero.")
        else:
            with st.spinner(f"Consultando bases de datos para {placa_input}..."):
                # LLAMADA A LA DATA REAL
                resultado = consultar_datos_vivos(placa_input, api_key)
                
                if isinstance(resultado, dict):
                    st.balloons()
                    # MUESTRA DE DATOS REALES EN TU PLANTILLA
                    st.markdown(f"### ✅ Resultados para la Placa: {placa_input}")
                    
                    with st.container(border=True):
                        c1, c2 = st.columns(2)
                        with c1:
                            st.write(f"**Aseguradora:** {resultado.get('companiaNombre')}")
                            st.write(f"**Estado:** {resultado.get('estadoDescripcion')}")
                        with c2:
                            st.write(f"**Inicio:** {resultado.get('fechaInicio')}")
                            st.write(f"**Fin:** {resultado.get('fechaFin')}")
                    
                    # Aquí es donde la info CAMBIA según la placa
                    st.info(f"Certificado N°: {resultado.get('numeroCertificado')}")
                else:
                    st.error(resultado)
