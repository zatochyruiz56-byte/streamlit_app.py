import streamlit as st
import streamlit.components.v1 as components

def run():
    # Título de tu App
    st.markdown("<h1 style='text-align: center; color: #000000;'>⚡ ZTCHY PRO: Panel de Control</h1>", unsafe_allow_html=True)

    # --- CONTENEDOR DEL DISFRAZ ---
    html_ztchy_pro = """
    <div style="
        width: 100%; 
        height: 480px; 
        overflow: hidden; 
        border: 3px solid #000000; 
        border-radius: 10px; 
        position: relative; 
        background: #000000;"> <div style="
            position: absolute; 
            top: 55px; 
            left: 50%; 
            transform: translateX(-50%);
            width: 300px; 
            height: 50px; 
            background: #ffffff; 
            z-index: 20; 
            display: flex; 
            align-items: center; 
            justify-content: center;
            font-family: Arial, sans-serif;
            font-weight: bold;
            font-size: 24px;
            color: #1E3A8A; 
            border-radius: 5px;">
            ZTCHY PRO
        </div>

        <iframe 
            src="https://www.apeseg.org.pe/consultas-soat/" 
            style="
                width: 1000px; 
                height: 1500px; 
                position: absolute; 
                top: -560px; /* Tus coordenadas exactas */
                left: 60%;  /* Tus coordenadas exactas */
                margin-left: -400px; 
                border: none;
                /* Filtro para convertir morados en azules oscuros y aumentar contraste con negro */
                filter: hue-rotate(240deg) brightness(0.9) contrast(120%) saturate(140%);
            "
            scrolling="no">
        </iframe>
    </div>
    """
    
    st.markdown("### 🔍 Validación de Seguridad")
    components.html(html_ztchy_pro, height=500)
    
    # Pie de página personalizado
    st.caption("🛡️ Pasarela Segura Ztchy Pro - Todos los derechos reservados 2026")

if __name__ == "__main__":
    run()
