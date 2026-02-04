import streamlit as st
import streamlit.components.v1 as components

def run():
    st.markdown("<h1 style='text-align: center; color: #000000;'>⚡ ZTCHY PRO SYSTEM</h1>", unsafe_allow_html=True)

    # --- CONTENEDOR MAESTRO ---
    html_ztchy_final = """
    <div style="
        width: 100%; 
        height: 520px; 
        overflow: hidden; 
        border: 5px solid #000000; 
        border-radius: 15px; 
        position: relative; 
        background: #000000;"> <div style="
            position: absolute; 
            top: 155px; /* Bajado estratégicamente para cubrir las letras */
            left: 50%; 
            transform: translateX(-50%);
            width: 320px; 
            height: 60px; 
            background: #ffffff; /* Mismo blanco que el fondo del formulario */
            z-index: 100; 
            display: flex; 
            align-items: center; 
            justify-content: center;
            box-shadow: 0px 2px 5px rgba(0,0,0,0.1);">
            <span style="
                font-family: 'Arial Black', Gadget, sans-serif; 
                font-size: 28px; 
                color: #003366; /* Azul Oscuro Ztchy */
                font-weight: bold;
                letter-spacing: -1px;">
                ZTCHY PRO
            </span>
        </div>

        <iframe 
            src="https://www.apeseg.org.pe/consultas-soat/" 
            style="
                width: 1000px; 
                height: 1500px; 
                position: absolute; 
                top: -560px; /* Tus coordenadas originales */
                left: 60%; 
                margin-left: -400px; 
                border: none;
                /* Filtro para eliminar verdes y dejar solo Azul y Negro */
                filter: hue-rotate(220deg) brightness(0.7) contrast(140%) saturate(180%);
            "
            scrolling="no">
        </iframe>
    </div>
    """
    
    st.markdown("### 🔑 Acceso a Base de Datos Privada")
    components.html(html_ztchy_final, height=550)
    
    st.caption("🛡️ Plataforma blindada por Ztchy Pro. No se guardan registros de consulta.")

if __name__ == "__main__":
    run()
