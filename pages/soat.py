import streamlit as st
import streamlit.components.v1 as components

def run():
    # Configuración de estilo para centrar y profesionalizar la vista
    st.set_page_config(page_title="Consulta SOAT Pro", layout="wide")
    
    st.markdown("""
        <style>
        .main {
            background-color: #f5f7f9;
        }
        .stButton>button {
            width: 100%;
            border-radius: 5px;
            height: 3em;
            background-color: #007bff;
            color: white;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1 style='text-align: center; color: #1E3A8A;'>🛡️ Portal de Consulta SOAT</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Acceso directo a la base de datos oficial de Interseguro</p>", unsafe_allow_html=True)

    # Crear dos columnas: Una para las instrucciones y otra para el visualizador
    col_inst, col_view = st.columns([1, 2])

    with col_inst:
        st.subheader("📝 Instrucciones")
        st.info("""
        1. **Ubica el buscador** en el recuadro de la derecha.
        2. **Ingresa la placa** del vehículo.
        3. **Resuelve el Captcha** (No soy un robot) directamente ahí.
        4. **Visualiza los resultados** detallados sin salir de esta app.
        """)
        
        st.warning("⚠️ Nota: Si el recuadro derecho aparece en blanco, la página oficial está bloqueando la conexión 'espejo' por seguridad.")
        
        # Espacio para notas adicionales del administrador
        with st.expander("¿Por qué usar este método?"):
            st.write("Este método evita el uso de créditos de Seeker y garantiza que la información sea 100% real de la aseguradora.")

    with col_view:
        st.subheader("🔍 Buscador Oficial Integrado")
        
        # --- EL CÓDIGO ESPEJO (IFRAME) ---
        # Usamos la URL exacta que me proporcionaste
        url_interseguro = "https://www.interseguro.pe/soat/consulta-soat"
        
        try:
            # Renderizamos la página externa
            components.iframe(url_interseguro, height=700, scrolling=True)
        except Exception as e:
            st.error(f"No se pudo cargar el espejo: {e}")

    st.divider()
    st.caption("Byte-Consultas | Conexión directa con servidores de seguros v1.0")

if __name__ == "__main__":
    run()
