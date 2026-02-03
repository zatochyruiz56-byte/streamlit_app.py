import streamlit as st
import requests
import json

def run():
    st.title("🌳 Árbol Familiar")
    st.info("Consulta de vínculos parentales (Padres, Hijos, Cónyuge) mediante DNI.")

    # Parámetros técnicos
    API_URL = "https://seeker-v6.com/personas/arbol-familiar"
    TOKEN = "sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"

    dni = st.text_input("DNI para Árbol Familiar", max_chars=8, placeholder="Ejm: 12345678")

    if st.button("🚀 GENERAR ÁRBOL", use_container_width=True):
        if not dni:
            st.warning("⚠️ Ingrese un DNI válido.")
            return

        headers = {"Authorization": f"Bearer {TOKEN}"}
        # IMPORTANTE: Este endpoint usa 'params' porque es un método GET
        params = {"dni": dni}

        try:
            with st.spinner("Rastreando vínculos genealógicos..."):
                response = requests.get(API_URL, headers=headers, params=params, timeout=25)
            
            # Diagnóstico rápido de respuesta
            if response.status_code == 200:
                try:
                    data = response.json()
                    
                    # 1. Mostrar JSON Crudo para ver la estructura
                    st.subheader("📦 Datos Crudos del Árbol")
                    st.code(json.dumps(data, indent=4, ensure_ascii=False), language="json")

                    # 2. Renderizado Visual (Si la API responde con éxito)
                    if data.get("status") == "success":
                        st.divider()
                        st.subheader("👥 Vínculos Detectados")
                        
                        vinc = data.get("data", {})
                        
                        # Creamos pestañas para organizar a la familia
                        t1, t2, t3 = st.tabs(["Padres", "Hijos", "Cónyuge/Otros"])
                        
                        with t1:
                            padres = vinc.get("padres", [])
                            if padres:
                                for p in padres:
                                    st.write(f"👤 **{p.get('tipo', 'PADRE')}:** {p.get('nombre', 'N/A')}")
                            else:
                                st.write("No se registraron datos de progenitores.")

                        with t2:
                            hijos = vinc.get("hijos", [])
                            if hijos:
                                for h in hijos:
                                    st.success(f"👶 **HIJO(A):** {h.get('nombre', 'N/A')} (DNI: {h.get('dni', '---')})")
                            else:
                                st.write("No se detectaron hijos registrados.")
                        
                        with t3:
                            otros = vinc.get("conyuge", "No especificado")
                            st.write(f"💍 **Cónyuge:** {otros}")

                except Exception:
                    st.error("❌ Fallo al procesar el JSON. El servidor envió algo inesperado.")
                    st.code(response.text)
            
            elif response.status_code == 500:
                st.error("🔥 Error 500: El servidor de Árbol Familiar está caído actualmente.")
                st.info("Esto suele pasar cuando la base de datos de RENIEC está saturada.")
            else:
                st.error(f"⚠️ Error {response.status_code}")
                st.code(response.text)

        except Exception as e:
            st.error(f"🔥 Error de conexión: {str(e)}")

if __name__ == "__main__":
    run()
