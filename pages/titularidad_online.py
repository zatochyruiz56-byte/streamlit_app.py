import streamlit as st
import requests
import json

def run():
    st.set_page_config(page_title="API Debugger Multifunción", layout="wide")
    
    st.title("🛠️ API Debugger Multifunción")
    st.info("Este módulo analiza la respuesta real del servidor para detectar bloqueos o errores de formato.")

    # Configuración de la petición
    with st.sidebar:
        st.header("Configuración de Red")
        API_URL = st.text_input("URL del Endpoint", "https://seeker-v6.com/telefonos/titularidad")
        TOKEN = "sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"
        metodo = st.selectbox("Método", ["POST", "GET"])

    dni = st.text_input("DNI de prueba", max_chars=8, placeholder="Ejm: 12345678")

    if st.button("🚀 LANZAR PETICIÓN Y ANALIZAR"):
        if not dni:
            st.warning("Ingrese un valor para probar.")
            return

        headers = {
            "Authorization": f"Bearer {TOKEN}",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0" # Simulamos un navegador para evitar bloqueos
        }
        
        payload = {"doc": dni}

        try:
            with st.spinner("Estableciendo conexión..."):
                if metodo == "POST":
                    response = requests.post(API_URL, json=payload, headers=headers, timeout=10)
                else:
                    response = requests.get(API_URL, headers=headers, params=payload, timeout=10)

            # --- PANEL DE DIAGNÓSTICO ---
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Código HTTP", response.status_code)
                if response.status_code == 200:
                    st.success("Conexión Exitosa")
                else:
                    st.error("Error de Acceso")

            with col2:
                tipo_cont = response.headers.get("Content-Type", "Desconocido")
                st.metric("Tipo de Contenido", tipo_cont.split(";")[0])
                
            with col3:
                tamaño = len(response.content)
                st.metric("Tamaño Respuesta", f"{tamaño} bytes")

            st.divider()

            # --- ANÁLISIS DE LA RESPUESTA ---
            st.subheader("📦 Cuerpo de la Respuesta")

            if "application/json" in tipo_cont:
                try:
                    data = response.json()
                    st.json(data)
                except Exception:
                    st.error("❌ El servidor dice que es JSON, pero el formato es inválido.")
                    st.code(response.text, language="text")
            else:
                st.warning("⚠️ El servidor envió HTML (Posible redirección o bloqueo de cuenta).")
                # Si es HTML, mostramos el código para leer el error real
                with st.expander("Ver Código Fuente de la Respuesta"):
                    st.code(response.text, language="html")
                
                # Intentamos extraer un mensaje de error si es una página web
                if "login" in response.text.lower():
                    st.error("💡 Diagnóstico: El servidor te está redirigiendo al LOGIN. Tu Token no tiene acceso a este módulo.")
                elif "error" in response.text.lower():
                    st.error("💡 Diagnóstico: Se detectó un error interno en la página del servidor.")

        except requests.exceptions.Timeout:
            st.error("🔥 Error: El servidor tardó demasiado en responder (Timeout).")
        except Exception as e:
            st.error(f"🔥 Error Crítico: {str(e)}")

if __name__ == "__main__":
    run()
