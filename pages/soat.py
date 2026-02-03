import streamlit as st
import streamlit.components.v1 as components

def run():
    st.markdown("<h3 style='text-align: center;'>🛡️ Consulta SOAT Instantánea</h3>", unsafe_allow_html=True)

    # --- CONFIGURACIÓN DE LA MÁSCARA FIJA ---
    # top: Ajusta qué tan arriba empieza el recorte (para ocultar el logo)
    # height: Altura del contenedor (la 'ventana' que ve el usuario)
    # scrolling="no": Desactiva el scroll del navegador en el iframe
    
    recorte_fijo_css = """
    <style>
        .portal-container {
            width: 100%;
            height: 420px; /* Altura justa para el formulario y el botón */
            overflow: hidden; /* Elimina el scroll del contenedor */
            border: 1px solid #d1d5db;
            border-radius: 12px;
            position: relative;
            background-color: white;
            box-shadow: 0px 4px 10px rgba(0,0,0,0.05);
        }
        .portal-container iframe {
            position: absolute;
            top: -385px; /* Sube la página para ocultar el encabezado */
            left: 50%;
            transform: translateX(-50%); /* Centra el contenido horizontalmente */
            width: 1200px; /* Ancho mayor para capturar el centro de la web original */
            height: 1500px;
        }
    </style>
    <div class="portal-container">
        <iframe 
            src="https://www.apeseg.org.pe/consultas-soat/" 
            frameborder="0" 
            scrolling="no"> 
        </iframe>
    </div>
    """

    # Renderizamos el recorte
    components.html(recorte_fijo_css, height=430)

    st.caption("⚠️ Nota: Resuelve el captcha dentro del cuadro. El resultado aparecerá en este mismo espacio.")

if __name__ == "__main__":
    run()
