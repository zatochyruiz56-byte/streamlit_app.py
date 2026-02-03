try:
    response = requests.post(API_URL, json=payload, headers=headers)
    
    # 1. Ver el código de estado (Ej: 401, 403, 500)
    st.write(f"Código de estado: {response.status_code}")
    
    # 2. Intentar ver el JSON si existe
    try:
        data = response.json()
        st.json(data) # Esto te mostrará el 'message' exacto de la API
    except:
        # 3. Si no es JSON, mostrar el texto crudo (aquí verás el error real)
        st.warning("La respuesta no es JSON. Mostrando contenido crudo:")
        st.code(response.text) 

except Exception as e:
    st.error(f"Fallo crítico de red: {str(e)}")
