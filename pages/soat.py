import streamlit as st
import streamlit.components.v1 as components

def run():
    st.markdown("<h2 style='text-align: center;'>🔍 Central de Consultas SOAT</h2>", unsafe_allow_html=True)
    
    # Creamos dos pestañas para no saturar la pantalla
    tab1, tab2 = st.tabs(["📊 Historial General (APESEG)", "📄 Descarga de PDF (Pacífico)"])

    with tab1:
        st.caption("Usa este panel para ver la vigencia y el historial de certificados.")
        # Ajuste para APESEG (según tus capturas de pantalla)
        html_apeseg = """
        <div style="width: 100%; height: 500px; overflow: hidden; border: 2px solid #1E3A8A; border-radius: 10px; position: relative;">
            <iframe src="https://www.apeseg.org.pe/consultas-soat/" 
                style="width: 1000px; height: 1200px; position: absolute; top: -385px; left: 50%; margin-left: -500px; border: none;"
                scrolling="no"></iframe>
        </div>
        """
        components.html(html_apeseg, height=520)

    with tab2:
        st.caption("Si el SOAT es de Pacífico, aquí podrás descargar el certificado oficial.")
        # Ajuste para Pacífico Seguros
        # top: -250px suele ocultar el banner principal de Pacífico
        html_pacifico = """
        <div style="width: 100%; height: 500px; overflow: hidden; border: 2px solid #0096d2; border-radius: 10px; position: relative;">
            <iframe src="https://www.pacifico.com.pe/consulta-soat" 
                style="width: 1000px; height: 1200px; position: absolute; top: -280px; left: 50%; margin-left: -500px; border: none;"
                scrolling="no"></iframe>
        </div>
        """
        components.html(html_pacifico, height=520)

    st.success("✅ Ambas consultas se realizan en tiempo real desde las fuentes oficiales.")

if __name__ == "__main__":
    run()
