import streamlit as st
import requests
import json

def run():
    st.set_page_config(page_title="Multifunción Teléfonos", layout="wide")
    
    st.title("📲 Multifunción de Teléfonos")
    st.markdown("---")

    # Configuración de los nuevos parámetros en el lateral
    with st.sidebar:
        st.header("⚙️ Parámetros de API")
        API_URL = "https://seeker-v6.com/telefonos/multifuncion_telefonos"
        TOKEN = "sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"
        
        # Aquí puedes definir los tipos que permite tu API (ejm: 'dni', 'nombre', 'celular')
        tipo_consulta = st.selectbox("Tipo de Búsqueda", ["dni", "nombre", "celular"])
        st.info("El parámetro 'tipo' ayuda a la API a identificar el origen de la búsqueda.")

    # Input principal
    valor_busqueda = st.text_input(f"Ingrese el valor para {tipo_consulta}", placeholder="Ejm: 12345678")

    if st.button("🚀 LANZAR CONSULTA MULTIFUNCIÓN", use_container_width=True):
        if not valor_busqueda:
            st.warning("Debe ingresar un valor para buscar.")
            return

        headers = {
            "Authorization": f"Bearer {TOKEN}",
            "Content-Type": "application/json"
        }
        
        # Payload exacto según tu nuevo requerimiento
        payload = {
            "doc": valor_busqueda,
            "tipo": tipo_consulta
        }

        try:
            with st.spinner("Conectando con el endpoint multifunción..."):
                response = requests.post(API_URL, json=payload, headers=headers, timeout=15)
            
            # Análisis de Respuesta
            st.subheader("📊 Análisis de la Respuesta")
            
            c1, c2 = st.columns(2)
            c1.metric("Código HTTP", response.status_code)
            c2.write(f"**Content-Type:** `{response.headers.get('Content-Type')}`")

            st.divider()

            # Lógica para mostrar JSON o Error
            if "application/json" in response.headers.get("Content-Type", ""):
                try:
                    data = response.json()
                    st.markdown("### 📦 JSON Data (Respuesta Cruda)")
                    st.code(json.dumps(data, indent=4, ensure_ascii=False), language="json")
                    
                    # Si la respuesta es exitosa, podrías mostrar un resumen rápido
                    if data.get("status") == "success":
                        st.success("API respondió con éxito.")
                except Exception:
                    st.error("Error al decodificar el JSON del servidor.")
                    st.code(response.text)
            else:
                st.warning("⚠️ El servidor no devolvió un JSON. Posible error de permisos o módulo caído.")
                with st.expander("Ver Respuesta HTML/Texto"):
                    st.code(response.text, language="html")

        except Exception as e:
            st.error(f"🔥 Error de conexión: {str(e)}")

if __name__ == "__main__":
    run()
