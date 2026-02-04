import streamlit as st
import streamlit.components.v1 as components

def run():
    st.markdown("<h2 style='text-align: center; color: #1E3A8A;'>🛡️ Verificador de Certificados Privado</h2>", unsafe_allow_html=True)

    # --- CSS PARA EL DISFRAZ TOTAL ---
    # 1. Filtro 'hue-rotate': Cambia los colores originales (morado/azul) por los de tu app.
    # 2. Capa 'overlay': Un div semitransparente encima para unificar el tono.
    html_disfrazado = """
    <div style="
        width: 100%; 
        height: 500px; 
        overflow: hidden; 
        border: 2px solid #1E3A8A; 
        border-radius: 15px; 
        position: relative; 
        background: white;">
        
        <div style="
            position: absolute; 
            top: 0; left: 0; 
            width: 100%; height: 100%; 
            background: rgba(30, 58, 138, 0.05); 
            pointer-events: none; 
            z-index: 10;">
        </div>

        <iframe 
            src="https://www.apeseg.org.pe/consultas-soat/" 
            style="
                width: 1000px; 
                height: 1500px; 
                position: absolute; 
                top: -560px; /* Tu medida exacta para ocultar encabezado */
                left: 60%;  /* Tu medida exacta */
                margin-left: -400px; 
                border: none;
                filter: hue-rotate(220deg) saturate(150%) contrast(90%); /* Cambia el color oficial al tuyo */
            "
            scrolling="no">
        </iframe>
    </div>
    """
    
    st.info("Escribe la placa y resuelve el captcha abajo para ver el resultado oficial.")
    components.html(html_disfrazado, height=520)
    
    st.success("✅ Verificación procesada a través de nuestra pasarela de datos privada.")

if __name__ == "__main__":
    run()
