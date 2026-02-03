import streamlit as st
import requests
import pandas as pd

def consultar_interseguro(placa):
    # La URL interna que usa Interseguro para las consultas de SOAT
    url = f"https://www.interseguro.pe/soat/api/v1/soat/consultar-soat-vigente/{placa}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://www.interseguro.pe/soat/consulta-soat"
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                return {"status": "success", "data": data.get("data")}
            else:
                return {"status": "error", "message": "No se encontró información para esa placa."}
        else:
            return {"status": "error", "message": f"Error del servidor de Interseguro ({response.status_code})"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def run():
    st.markdown("<h1 style='text-align: center;'>🛡️ Consulta SOAT Interseguro</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Fuente: Interseguro (Oficial)</p>", unsafe_allow_html=True)

    placa = st.text_input("Ingrese Placa (ej: ABC123)", max_chars=6).upper()

    if st.button("📊 OBTENER INFORMACIÓN DETALLADA", use_container_width=True):
        if not placa:
            st.warning("Por favor, ingrese una placa.")
            return

        with st.spinner(f"Consultando base de datos de Interseguro para la placa {placa}..."):
            res = consultar_interseguro(placa)
            
            if res["status"] == "success":
                info = res["data"]
                st.balloons()
                
                # --- DISEÑO DE INFORMACIÓN DETALLADA ---
                st.markdown("### 📋 Resultados de la Póliza")
                
                with st.container(border=True):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**🔹 Aseguradora:** {info.get('companiaNombre', 'N/A')}")
                        st.write(f"**🔹 Estado:** {info.get('estadoDescripcion', 'N/A')}")
                        st.write(f"**🔹 Nro. Póliza:** {info.get('numeroCertificado', 'N/A')}")
                    
                    with col2:
                        st.write(f"**📅 Inicio:** {info.get('fechaInicio', 'N/A')}")
                        st.write(f"**📅 Fin:** {info.get('fechaFin', 'N/A')}")
                        st.write(f"**🚗 Uso:** {info.get('usoDescripcion', 'N/A')}")
                
                # Información extra si está disponible
                if info.get('claseDescripcion'):
                    st.info(f"💡 **Tipo de Vehículo:** {info.get('claseDescripcion')}")
                
                st.success("✅ Información obtenida exitosamente y sin costo de créditos.")
            else:
                st.error(res["message"])

if __name__ == "__main__":
    run()
