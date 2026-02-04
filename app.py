import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# Inicializar Firebase con los secretos cargados
if not firebase_admin._apps:
    # Cargamos el diccionario desde st.secrets
    creds_dict = dict(st.secrets["firebase"])
    # Corregimos los saltos de línea de la llave privada
    creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n")
    
    cred = credentials.Certificate(creds_dict)
    firebase_admin.initialize_app(cred)

db = firestore.client()
