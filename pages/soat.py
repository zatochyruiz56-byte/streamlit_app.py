import streamlit as st
import streamlit.components.v1 as components

def run():
    st.title("🛡️ Sistema Privado de Verificación")
    
    # --- CSS para ocultar rastros de la fuente ---
    st.markdown("""
        <style>
        .fuente-oculta {
            pointer-events: none; /* Evita que hagan clic en logos */
            user-select: none;
        }
        </style>
    """, unsafe_allow_html=True)

    # --- APESEG DISFRAZADO (Con tus medidas exactas) ---
    # Usamos un contenedor que corta los bordes donde suelen estar los logos
    html_disfraz = """
    <div style="width: 100%; height: 420px; overflow: hidden; border: 1px solid #ddd; border-radius: 15px; position: relative;">
        <iframe 
            src="https://www.apeseg.org.pe/consultas-soat/" 
            style="
                width: 900px; 
                height: 1200px; 
                position: absolute; 
                top: -560px; /* Tu medida exacta */
                left: 60%;  /* Tu medida exacta */
                margin-left: -400px; /* Tu medida exacta */
                border: none;
                filter: contrast(110%); /* Un pequeño filtro para que cambie el tono original */
            "
            scrolling="no">
        </iframe>
    </div>
    """
    
    st.markdown("### Ingrese Placa para Validación")
    components.html(html_disfraz, height=450)

    # --- MENSAJE PERSONALIZADO ---
    st.caption("✅ Verificación procesada a través de nuestra pasarela de datos privada.")

if __name__ == "__main__":
    run()
