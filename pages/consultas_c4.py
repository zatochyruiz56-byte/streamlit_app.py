# ... (dentro del bloque try después de requests.post)
                response = requests.post(API_URL, json=payload, headers=headers)
                
                # Esto te dirá el código de estado exacto (ej. 401, 404, 500)
                st.write(f"Código de estado HTTP: {response.status_code}")

                try:
                    data = response.json()
                except Exception:
                    st.error("La respuesta no es un JSON válido")
                    st.text(response.text) # Muestra el HTML/Texto crudo si falla el JSON
                    return

                if response.status_code == 200:
                    if data.get("status") == "success":
                        st.success("¡Datos encontrados!")
                        st.json(data.get("data"))
                    else:
                        st.error(f"Error de la API: {data.get('message')}")
                elif response.status_code == 401:
                    st.error("Token inválido o expirado.")
                elif response.status_code == 429:
                    st.error("Has superado el límite de peticiones (Rate Limit).")
                else:
                    st.error("Error desconocido en el servidor externo.")
                
                # Muestra TODO lo que devuelve la API para no perder detalles
                with st.expander("Inspección completa de respuesta"):
                    st.write("Headers de respuesta:", response.headers)
                    st.write("Cuerpo completo:", data)
