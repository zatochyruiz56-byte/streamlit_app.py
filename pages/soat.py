import streamlit as st
import requests

def consultar_interseguro_detallado(placa):
    # Endpoint real de la API de Interseguro
    url = f"https://www.interseguro.pe/soat/api/v1/soat/consultar-soat-vigente/{placa}"
    
    # Headers de alta prioridad para saltar bloqueos
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Origin": "https://www.interseguro.pe",
        "Referer": "https://www.interseguro.pe/soat/consulta-soat",
        "Accept-Language": "es-ES,es;q=0.9",
    }

    try:
        # Hacemos la petición simulando ser el sitio web
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                return {"status": "success", "data": data.get("data")}
            else:
                return {"status": "error", "message": "Placa no encontrada en Interseguro."}
        elif response.status_code == 403:
            return {"status": "error", "message": "Acceso denegado (El servidor detectó el script)."}
        else:
            return {"status": "error", "message": f"Error servidor ({response.status_code})"}
            
    except Exception as e:
        return {"status": "error", "message": f"Conexión fallida: {str(e)}"}

def run():
    st.markdown("### 🛡️ Extractor Detallado de SOAT")
    st.caption("Fuente: Interseguro Directo (Bypass Seeker)")

    placa = st.text_input("Ingrese Placa para el Puente", max_chars=6, placeholder="M3Z244").upper()

    if st.button("🔍 EXTRAER DATOS VIVOS"):
        if not placa:
            st.error("Ingresa una placa.")
            return

        with st.spinner("Bypassing seguridad de Interseguro..."):
            res = consultar_interseguro_detallado(placa)
            
            if res["status"] == "success":
                info = res["data"]
                st.balloons()
                
                # Diseño de ficha detallada
                with st.container(border=True):
                    st.subheader(f"📄 Certificado: {info.get('numeroCertificado', 'S/N')}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f"**Aseguradora:** {info.get('companiaNombre')}")
                        st.markdown(f"**Estado:** `{info.get('estadoDescripcion')}`")
                        st.markdown(f"**Uso:** {info.get('usoDescripcion')}")
                    
                    with col2:
                        st.markdown(f"**Vence el:** {info.get('fechaFin')}")
                        st.markdown(f"**Inició el:** {info.get('fechaInicio')}")
                        st.markdown(f"**Clase:** {info.get('claseDescripcion', 'N/A')}")
                
                # Mostramos el JSON crudo por si quieres ver más campos ocultos
                with st.expander("Ver toda la data extraída"):
                    st.json(info)
            else:
                st.error(f"❌ No se pudo obtener: {res['message']}")
                st.info("Nota: Algunas aseguradoras bloquean consultas externas masivas.")

if __name__ == "__main__":
    run()
