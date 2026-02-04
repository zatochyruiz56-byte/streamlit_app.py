import streamlit as st

# ... (Tu código de conexión a Firebase arriba) ...

if not st.session_state.user:
    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    st.title("🚀 ZTCHY PRO")
    
    client_id = st.secrets["google_client_id"]
    redirect_uri = "https://appappppy-43nnqkr6ctadmkdomd2nxc.streamlit.app/"
    
    # URL de autenticación optimizada
    auth_url = (
        f"https://accounts.google.com/o/oauth2/v2/auth?"
        f"client_id={client_id}&"
        f"response_type=code&"
        f"scope=openid%20email%20profile&"
        f"redirect_uri={redirect_uri}&"
        f"prompt=select_account"
    )

    # ESTO ES LO QUE HACE QUE NO ABRA OTRA PESTAÑA
    # Usamos un componente de link que actúa sobre la ventana actual (_self)
    st.markdown(
        f"""
        <a href="{auth_url}" target="_self" style="
            text-decoration: none;
            display: inline-block;
            padding: 0.5em 1em;
            color: white;
            background-color: #4285F4;
            border-radius: 10px;
            width: 100%;
            text-align: center;
            font-weight: bold;
        ">🌐 Ingresar con Google</a>
        """,
        unsafe_allow_html=True
    )

    st.write("---")
    # ... (Login manual de ZATOCHY) ...
