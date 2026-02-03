import streamlit as st
import streamlit.components.v1 as components

def run():
    st.set_page_config(page_title="Consulta SOAT Compacta", layout="centered")

    st.markdown("<h2 style='text-align: center;'>📄 Consulta Directa APESEG</h2>", unsafe_allow_html=True)
    st.caption("Resuelve el captcha en el recuadro para ver el estado de vigencia.")

    # --- TRUCO DE RECORTE (CSS) ---
    # Creamos un contenedor con 'overflow: hidden' para ocultar lo que no queremos ver.
    # El iframe se desplaza hacia arriba con un margen negativo para centrar el formulario.
    recorte_css = """
    <style>
        .iframe-container {
            width: 100%;
            height: 500px;
            overflow: hidden;
            border: 2px solid #e6e9ef;
            border-radius: 10px;
            position: relative;
            background: white;
        }
        .iframe-container iframe {
            position: absolute;
            top: -380px; /* Ajusta este valor para subir/bajar el recorte superior */
            left: -10px;
            width: 100%;
            height: 1200px; /* Altura total para permitir el scroll interno */
        }
    </style>
    <div class="iframe-container">
        <iframe src="https://www.apeseg.org.pe/consultas-soat/" frameborder="0"></iframe>
    </div>
    """

    # Renderizamos el componente con el recorte
    components.html(recorte_css, height=520)

    st.success("✅ Una vez que des clic en 'Consultar', desplázate dentro del cuadro para ver el resultado.")

if __name__ == "__main__":
    run()
