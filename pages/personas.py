import streamlit as st
import requests

# 1. Configuración y Seguridad
st.set_page_config(page_title="DataAPI - Consulta Premium", layout="wide")

if not st.session_state.get('auth', False):
    st.error("⚠️ Acceso denegado.")
    st.stop()

# Estilo para los "cajoncitos" de información
st.markdown("""
    <style>
    .info-box {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 10px;
    }
    .label { color: #8b949e; font-size: 12px; margin-bottom: 5px; }
    .value { color: #ffffff; font-size: 16px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("👤 Consulta de Persona - Premium")

# Selector de tipo de búsqueda
opcion = st.radio("Seleccione servicio:", ["DNI Premium", "Nombres (Próximamente)"], horizontal=True)

dni_input = st.text_input("Ingrese número de DNI:", max_chars=8)

if st.button("BUSCAR INFORMACIÓN"):
    if len(dni_input) == 8:
        TOKEN = "sk_live_104655a1666c3ea084ecc19f6b859a5fbb843f0aaac534ad"
        URL = "https://seeker-v6.com/personas/apiPremium/dni"
        
        with st.spinner("Extrayendo datos de la base de datos..."):
            try:
                r = requests.post(URL, headers={"Authorization": f"Bearer {TOKEN}"}, data={"dni": dni_input})
                res = r.json()
                
                if res.get("status") == "success":
                    data = res.get("data", {})
                    
                    st.success("Resultados encontrados")
                    st.markdown("---")
                    
                    # --- DISEÑO DE LA INFORMACIÓN (Como la página original) ---
                    col_foto, col_datos = st.columns([1, 3])
                    
                    with col_foto:
                        st.subheader("📷 Fotografía")
                        # Intentamos mostrar la foto. La API suele enviarla en 'foto' o 'foto_base64'
                        foto_data = data.get("foto") or data.get("foto_base64")
                        if foto_data:
                            # Si es base64, Streamlit lo reconoce así:
                            if "data:image" in str(foto_data):
                                st.image(foto_data, width=200)
                            else:
                                st.image(foto_data, width=200)
                        else:
                            st.warning("Foto no disponible")

                    with col_datos:
                        st.subheader("📝 Datos Personales")
                        # Creamos los cajoncitos en cuadrícula
                        c1, c2, c3 = st.columns(3)
                        
                        fields = [
                            ("NOMBRES", data.get("nombres")),
                            ("APELLIDO PATERNO", data.get("apellido_paterno")),
                            ("APELLIDO MATERNO", data.get("apellido_materno")),
                            ("FECHA NACIMIENTO", data.get("fecha_nacimiento")),
                            ("ESTADO CIVIL", data.get("estado_civil")),
                            ("SEXO", data.get("sexo")),
                            ("UBIGEO", data.get("ubigeo_nacimiento")),
                            ("DEPARTAMENTO", data.get("departamento")),
                            ("PROVINCIA", data.get("provincia")),
                            ("DISTRITO", data.get("distrito")),
                            ("DIRECCIÓN", data.get("direccion")),
                        ]
                        
                        # Distribución automática en cajoncitos
                        for i, (label, value) in enumerate(fields):
                            target_col = [c1, c2, c3][i % 3]
                            target_col.markdown(f"""
                                <div class="info-box">
                                    <div class="label">{label}</div>
                                    <div class="value">{value if value else '---'}</div>
                                </div>
                            """, unsafe_allow_html=True)
                            
                    # Datos de los padres (Si la API los da)
                    if data.get("nombre_padre") or data.get("nombre_madre"):
                        st.markdown("---")
                        st.subheader("👪 Datos Familiares")
                        f1, f2 = st.columns(2)
                        f1.markdown(f'<div class="info-box"><div class="label">PADRE</div><div class="value">{data.get("nombre_padre")}</div></div>', unsafe_allow_html=True)
                        f2.markdown(f'<div class="info-box"><div class="label">MADRE</div><div class="value">{data.get("nombre_madre")}</div></div>', unsafe_allow_html=True)

                else:
                    st.error(f"Error: {res.get('message', 'No se encontró el DNI')}")
            except Exception as e:
                st.error(f"Fallo en la consulta: {e}")
    else:
        st.warning("DNI debe tener 8 números.")

if st.button("🔙 Volver"):
    st.switch_page("app.py")
