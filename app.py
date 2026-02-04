import streamlit as st

# ... (Mantén tu conexión a Firebase aquí arriba) ...

if not st.session_state.user:
    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    st.title("🚀 ZTCHY PRO")
    
    # Esta función de Streamlit crea una ventana "encima" de la app
    @st.dialog("Iniciar Sesión con Google")
    def login_popup():
        st.write("Haz clic abajo para autenticarte:")
        client_id = st.secrets["google_client_id"]
        redirect_uri = "https://appappppy-43nnqkr6ctadmkdomd2nxc.streamlit.app/"
        auth_url = f"https://accounts.google.com/o/oauth2/v2/auth?client_id={client_id}&response_type=code&scope=openid%20email%20profile&redirect_uri={redirect_uri}"
        
        # El target="_self" intenta cargar la respuesta en el mismo marco
        st.link_button("🌐 Ir a Google", auth_url, use_container_width=True)

    if st.button("🌐 Ingresar con Google", use_container_width=True):
        login_popup()

    st.write("---")
    # ... (Resto de tu login manual para ZATOCHY) ...
