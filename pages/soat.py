import streamlit as st
import requests

def run():
    st.title("🛡️ SOAT: Consulta con Validación Humana")
    
    st.markdown("""
    ### Paso 1: Valida que eres humano
    Resuelve el captcha en el recuadro de abajo. Una vez que la página de Interseguro 
    te permita ver los datos, presiona el botón **'Sincronizar Datos'** en nuestra app.
    """)

    # Mostramos la página oficial en un iframe para que el usuario interactúe
    st.components.v1.iframe("https://www.interseguro.pe/soat/consulta-soat", height=500, scrolling=True)

    st.divider()

    # Paso 2: El usuario ingresa la placa aquí después de validar
    placa = st.text_input("Paso 2: Ingrese la placa validada", max_chars=6).upper()

    if st.button("🔄 SINCRONIZAR Y EXTRAER DETALLES"):
        if not placa:
            st.warning("Primero ingresa la placa.")
        else:
            with st.spinner("Intentando extraer datos de la sesión validada..."):
                # Aquí intentamos el bypass con los headers reforzados
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/121.0.0.0",
                    "Referer": "https://www.interseguro.pe/soat/consulta-soat",
                }
                url = f"https://www.interseguro.pe/soat/api/v1/soat/consultar-soat-vigente/{placa}"
                
                try:
                    res = requests.get(url, headers=headers)
                    if res.status_code == 200 and res.json().get("success"):
                        data = res.json()["data"]
                        st.success("¡Datos sincronizados!")
                        st.json(data) # Aquí mostramos toda la info detallada
                    else:
                        st.error("El servidor aún pide validación. ¿Resolviste el captcha en el recuadro de arriba?")
                except:
                    st.error("Error de conexión con el puente.")

if __name__ == "__main__":
    run()
