import streamlit as st
import streamlit.components.v1 as components

def run():
    st.markdown("<h2 style='text-align: center; color: #1E3A8A;'>📄 Descarga de SOAT Electrónico</h2>", unsafe_allow_html=True)
    st.info("Esta plataforma permite obtener el certificado digital de Interseguro y otras compañías vinculadas.")

    # --- ESPEJO DE INTERSEGURO (ZONA DE DESCARGA) ---
    # Ajustado para centrar el buscador de certificados
    html_descarga = """
    <div style="
        width: 100%; 
        height: 550px; 
        overflow: hidden; 
        border: 2px solid #00ac4e; 
        border-radius: 12px; 
        position: relative;
        background: white;">
        
        <iframe 
            src="https://www.interseguro.pe/soat/consulta-soat" 
            style="
                width: 1000px; 
                height: 1500px; 
                position: absolute; 
                top: -320px; /* Ajuste para saltar el banner y caer en el buscador */
                left: 50%; 
                margin-left: -500px; 
                border: none;
            "
            scrolling="no">
        </iframe>
    </div>
    """

    components.html(html_descarga, height=570)
    
    st.caption("Nota: Si el SOAT no es de esta aseguradora, el sistema te indicará a qué compañía pertenece.")

if __name__ == "__main__":
    run()
