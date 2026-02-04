import streamlit as st
import streamlit.components.v1 as components

def run():
    st.markdown("<h1 style='text-align: center; color: #000000;'>⚡ ZTCHY PRO SYSTEM</h1>", unsafe_allow_html=True)

    # --- CONTENEDOR DEL DISFRAZ ---
    html_ztchy_pro = """
    <div style="
        width: 100%; 
        height: 500px; 
        overflow: hidden; 
        border: 4px solid #000000; 
        border-radius: 12px; 
        position: relative; 
        background: #0d1117;"> <div style="
            position: absolute; 
            top: 98px; /* Ajustado para caer justo sobre el título original */
            left: 50%; 
            transform: translateX(-50%);
            width: 250px; 
            height: 45px; 
            background: #ffffff; /* Color del fondo del formulario para camuflaje */
            z-index: 100; 
            display: flex; 
            align-items: center; 
            justify-content: center;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            font-weight: 900;
            font-size: 26px;
            color: #1E3A8A; /* Azul Ztchy */
            letter-spacing: 1px;">
            ZTCHY PRO
        </div>

        <iframe 
            src="https://www.apeseg.org.pe/consultas-soat/" 
            style="
                width: 1000px; 
                height: 1500px; 
                position: absolute; 
                top: -560px; /* Tus coordenadas de recorte exactas */
                left: 60%; 
                margin-left: -400px; 
                border: none;
                /* Filtro: Convierte verdes/morados en azul profundo y sombras negras */
                filter: hue-rotate(220deg) brightness(0.8) contrast(130%) saturate(150%) invert(5%) grayscale(20%);
            "
            scrolling="no">
        </iframe>
    </div>
    """
    
    st.markdown("### 🔍 Panel de Validación Segura")
    components.html(html_ztchy_pro, height=530)
    
    st.caption("🔒 Acceso restringido - Pasarela de datos protegida por Ztchy Pro 2026")

if __name__ == "__main__":
    run()
