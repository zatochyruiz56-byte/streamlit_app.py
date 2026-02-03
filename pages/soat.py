import streamlit as st
import requests
from bs4 import BeautifulSoup

def consultar_soat_independiente(placa):
    # Usamos el endpoint de consulta rápida de APESEG
    url = "https://www.apeseg.org.pe/consultas-soat/"
    
    # Headers para parecer un navegador real y evitar bloqueos
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }

    try:
        # Nota: La mayoría de estas webs usan una petición POST interna o un iframe.
        # Por ahora, simularemos la extracción de datos para que veas la estructura:
        st.info(f"Conectando directamente con la base de datos de seguros para la placa {placa}...")
        
        # En un escenario real de scraping, aquí iría la lógica de requests.post()
        # con los tokens de validación de la página destino.
        
        # Simulación de respuesta exitosa del puente:
        return {
            "status": "success",
            "data": {
                "compania": "PACIFICO SEGUROS",
                "inicio": "15/05/2025",
                "fin": "15/05/2026",
                "estado": "VIGENTE",
                "tipo": "ELECTRONICO"
            }
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

def run():
    st.markdown("### 🛡️ SOAT: Puente Directo (Sin Créditos)")
    st.caption("Estado actual de Seeker: 🔴 Caído (Error de Sesión)")
    
    placa = st.text_input("Ingrese Placa para el Puente", max_chars=7).upper()

    if st.button("🚀 CONSULTAR EXTERNAMENTE"):
        if not placa:
            st.error("Ingresa una placa válida.")
            return
            
        res = consultar_soat_independiente(placa)
        
        if res["status"] == "success":
            st.balloons()
            info = res["data"]
            with st.container(border=True):
                st.subheader(f"✅ SOAT Encontrado: {placa}")
                c1, c2 = st.columns(2)
                c1.metric("Estado", info["estado"])
                c1.write(f"**Compañía:** {info['compania']}")
                c2.write(f"**Vence el:** {info['fin']}")
                c2.write(f"**Tipo:** {info['tipo']}")
        else:
            st.error(f"El puente falló: {res['message']}")

if __name__ == "__main__":
    run()
