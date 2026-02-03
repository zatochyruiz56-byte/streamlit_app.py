import streamlit as st

def run():
    st.title("🚗 Generador de Plantilla: Licencia")

    # MOCK DATA: Datos de ejemplo para que diseñes tu plantilla sin errores
    # Basado en los campos que suelen retornar estas APIs
    fake_data = {
        "nombres": "JUAN PABLO",
        "apellido_paterno": "PEREZ",
        "apellido_materno": "GARCIA",
        "licencia": "Q45106211",
        "clase": "A-I",
        "estado": "VIGENTE",
        "vencimiento": "15/05/2028",
        "puntos": "0"
    }

    dni = st.text_input("DNI para probar visualización", max_chars=8)

    if st.button("VER VISTA PREVIA DE PLANTILLA"):
        # DISEÑO DE TU PLANTILLA PROFESIONAL
        st.markdown("""
            <style>
            .licencia-card {
                background-color: #f0f2f6;
                padding: 20px;
                border-radius: 10px;
                border-left: 10px solid #007bff;
            }
            </style>
        """, unsafe_allow_html=True)

        with st.container():
            st.markdown(f"""
            <div class="licencia-card">
                <h3>SISTEMA DE LICENCIAS</h3>
                <p><b>Conductor:</b> {fake_data['nombres']} {fake_data['apellido_paterno']}</p>
                <p><b>Nro. Licencia:</b> {fake_data['licencia']}</p>
                <p><b>Clase/Cat:</b> {fake_data['clase']} | <b>Estado:</b> <span style="color:green">{fake_data['estado']}</span></p>
                <p><b>Vence:</b> {fake_data['vencimiento']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.success("Diseño cargado con datos de prueba. La API real está en mantenimiento.")

if __name__ == "__main__":
    run()
