import streamlit as st
import requests
import json

def run():
    st.title("🔍 Depuración de Datos - Factiliza")
    
    TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI0MDMwNSIsImh0dHA6Ly9zY2hlbWFzLm1pY3Jvc29mdC5jb20vd3MvMjAwOC8wNi9pZGVudGl0eS9jbGFpbXMvcm9sZSI6ImNvbnN1bHRvciJ9.Gsokm2AIDVCMdG5etymgkljwqXoCrb7b24c75H_VMr0"
    headers = {"Authorization": f"Bearer {TOKEN}"}
    dni = st.text_input("DNI para probar data cruda:", max_chars=8)

    if st.button("Obtener JSON Real"):
        url = f"https://api.factiliza.com/v1/licencia/info/{dni}"
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            raw_data = response.json()
            
            st.subheader("📦 Respuesta Completa de la API:")
            # Esto mostrará absolutamente todo lo que la API envía sin filtros
            st.json(raw_data) 
            
            st.divider()
            st.info("💡 Revisa los nombres de arriba. Si dice 'nombres' en lugar de 'full_name', debemos corregir el diseño.")
        else:
            st.error(f"Error {response.status_code}: {response.text}")

if __name__ == "__main__":
    run()
