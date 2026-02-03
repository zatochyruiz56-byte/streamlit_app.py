import streamlit as st
import requests

def run():
    st.title("📄 Generador de Plantillas RENIEC")
    
    # Configuración de API
    API_URL = "https://seeker-v6.com/personas/api/generadorplantillas"
    TOKEN = "sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"
    
    with st.sidebar:
        st.header("Configuración")
        tipo_plantilla = st.selectbox("Formato", ["completa", "basica", "moderna"])

    dni = st.text_input("Ingrese DNI", max_chars=8, placeholder="45106211")

    if st.button("🚀 GENERAR FICHA"):
        if len(dni) != 8:
            st.warning("⚠️ El DNI debe tener 8 dígitos.")
            return

        headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
        payload = {"dni": dni, "tipo": tipo_plantilla}

        try:
            with st.spinner("Consultando servidor..."):
                response = requests.post(API_URL, json=payload, headers=headers)
                data = response.json()

            # CASO 1: ÉXITO REAL
            if response.status_code == 200 and data.get("status") == "success":
                st.success("✅ Datos recuperados de la API")
                mostrar_ficha(data.get("data", {}), dni)

            # CASO 2: EL ERROR INTERNO QUE ESTÁS RECIBIENDO
            else:
                st.error(f"❌ Error de la API: {data.get('message', 'Error interno')}")
                st.info("💡 Mostrando VISTA PREVIA (Modo Simulación) para diseño:")
                
                # DATOS DE EJEMPLO PARA QUE NO TE QUEDES SIN VER NADA
                datos_ejemplo = {
                    "Nombres": "JUAN ALBERTO",
                    "Apellido Paterno": "PEREZ",
                    "Apellido Materno": "RODRIGUEZ",
                    "Fecha Nacimiento": "15/05/1985",
                    "Estado Civil": "SOLTERO",
                    "Dirección": "AV. LAS FLORES 123 - LIMA",
                    "Restricción": "NINGUNA"
                }
                mostrar_ficha(datos_ejemplo, dni)

        except Exception as e:
            st.error(f"🔥 Error de conexión: {str(e)}")

def mostrar_ficha(datos, dni):
    """Función para dibujar la ficha de forma elegante"""
    st.markdown(f"### 📋 Ficha de Identidad - DNI {dni}")
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    for i, (campo, valor) in enumerate(datos.items()):
        if i % 2 == 0:
            col1.info(f"**{campo}:** \n\n {valor}")
        else:
            col2.info(f"**{campo}:** \n\n {valor}")

if __name__ == "__main__":
    run()
