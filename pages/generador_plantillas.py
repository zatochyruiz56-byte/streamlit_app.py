import streamlit as st
import requests

def run():
    st.set_page_config(page_title="Generador de Plantillas", page_icon="📄")
    st.title("📄 Generador de Plantillas RENIEC")
    
    # Configuración de API basada en documentación
    API_URL = "https://seeker-v6.com/personas/api/generadorplantillas"
    TOKEN = "sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"
    
    with st.sidebar:
        st.header("Configuración")
        tipo_plantilla = st.selectbox(
            "Seleccione el Formato", 
            ["completa", "basica", "moderna"],
            help="Defina el nivel de detalle de la ficha"
        )

    dni = st.text_input("Ingrese el DNI a consultar", max_chars=8, placeholder="45106211")

    if st.button("🚀 GENERAR FICHA"):
        if len(dni) != 8:
            st.warning("⚠️ El DNI debe tener exactamente 8 dígitos.")
            return

        headers = {
            "Authorization": f"Bearer {TOKEN}",
            "Content-Type": "application/json"
        }
        payload = {
            "dni": dni,
            "tipo": tipo_plantilla
        }

        try:
            with st.spinner("Solicitando datos al servidor..."):
                response = requests.post(API_URL, json=payload, headers=headers)
                
                # Verificación de tipo de contenido
                if "application/json" not in response.headers.get("Content-Type", ""):
                    st.error("❌ El servidor devolvió un formato no válido (HTML).")
                    return

                data = response.json()

            # Procesamiento de la respuesta
            if response.status_code == 200 and data.get("status") == "success":
                st.success("✅ Datos recuperados con éxito")
                
                # --- DISEÑO DE LA PLANTILLA ---
                info = data.get("data", {})
                if info:
                    st.subheader(f"Ficha RENIEC - DNI {dni}")
                    cols = st.columns(2)
                    
                    # Mapeo de datos dinámico
                    for i, (clave, valor) in enumerate(info.items()):
                        col_idx = i % 2
                        cols[col_idx].text_input(clave.replace("_", " ").title(), value=valor, disabled=True)
                
                if "creditos_restantes" in data:
                    st.sidebar.metric("Créditos Restantes", data["creditos_restantes"])

            elif data.get("message") == "Error interno":
                st.error("❌ Error Interno del Servidor (Seeker-V6)")
                st.info("Este error indica que el DNI podría no estar en la base de datos de plantillas o el servicio está saturado. Intenta con 'basica'.")
            
            else:
                st.error(f"⚠️ Error de la API: {data.get('message', 'Error desconocido')}")

        except Exception as e:
            st.error(f"🔥 Error de conexión: {str(e)}")

if __name__ == "__main__":
    run()
