import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# Inicialización segura para Streamlit Cloud
if not firebase_admin._apps:
    # Usamos st.secrets para no exponer tu serviceAccount.json en GitHub
    creds_dict = dict(st.secrets["firebase"])
    # Esto corrige el formato de la llave privada de Google Cloud
    creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n")
    
    cred = credentials.Certificate(creds_dict)
    firebase_admin.initialize_app(cred)

db = firestore.client()
