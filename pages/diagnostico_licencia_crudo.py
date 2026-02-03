import streamlit as st
import requests
import streamlit.components.v1 as components

st.set_page_config(page_title="API Direct Inspector", layout="wide")

st.title("🔍 Inspector de Respuesta Directa")
st.write("Verás exactamente lo que el servidor 'Seeker' está escupiendo.")

col1, col2 = st.columns([1, 1])

with col1:
    dni = st.text_input("DNI", value="60799566")
with col2:
    tipo = st.selectbox("Tipo", ["BÁSICO", "COMPLETO"])

if st.button("INSPECCIONAR RESPUESTA", type="primary"):
    url = "https://seeker-v6.com/vehiculos/licencia_conductor"
    token = "sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    payload = {"dni": dni, "tipo": tipo}

    try:
        r = requests.post(url, headers=headers, json=payload, timeout=20)
        
        st.divider()
        st.subheader("📊 Datos Técnicos (Headers)")
        st.json(dict(r.headers))
        
        st.write(f"**Status Code:** {r.status_code}")
        st.write(f"**Content-Type:** {r.headers.get('Content-Type')}")

        st.divider()

        tab1, tab2, tab3 = st.tabs(["🌐 Vista Renderizada", "📄 Código Fuente (Raw)", "📦 JSON (Si aplica)"])

        with tab1:
            st.info("Así se vería la respuesta en un navegador:")
            # Renderizamos el HTML directamente en Streamlit
            components.html(r.text, height=600, scrolling=True)

        with tab2:
            st.info("Este es el código fuente exacto que llegó:")
            st.code(r.text, language="html")

        with tab3:
            try:
                st.json(r.json())
            except:
                st.warning("La respuesta no contiene un JSON válido.")

    except Exception as e:
        st.error(f"Error de conexión: {str(e)}")

st.caption("Usa la pestaña 'Vista Renderizada' para ver si es una página de error o login.")
