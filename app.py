import streamlit as st
from firestore_connection import db

st.set_page_config(
    page_title="Liga Agalu",
    page_icon=":soccer:",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Liga Agalu - Bem-vindo!")
st.write("Este é o sistema de gestão do campeonato, com estatísticas e cadastro de jogadores/rodadas.")
st.markdown("---")
st.markdown("Navegue pelas **páginas** no menu lateral ou na parte superior para acessar cada funcionalidade.")

# Exemplo de rodapé ou algo
st.markdown("© 2023 Liga Agalu")
