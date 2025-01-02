import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import json

@st.cache_resource
def init_connection():
    if not firebase_admin._apps:
        # Lê o JSON de credenciais a partir das secrets
        cred_dict = json.loads(st.secrets["FIREBASE_CRED"])
        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred)
    return firestore.client()

db = init_connection()
