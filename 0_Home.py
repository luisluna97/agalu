import streamlit as st
from firestore_connection import db

st.set_page_config(
    page_title="Liga Agalu",
    page_icon=":soccer:",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Liga Agalu")
st.write("A MAIOR LIGA DE FUTEBOL AMADOR DE RECIFE")
st.markdown("Toda quinta às 20h no PSG")
st.markdown("Navegue pelas **páginas** no menu lateral ou na parte superior para acessar cada funcionalidade.")

# Exemplo de rodapé ou algo
st.markdown("© 2022 Liga Agalu")
