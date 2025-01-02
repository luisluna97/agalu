import streamlit as st

st.set_page_config(
    page_title="Liga Agalu",
    page_icon=":soccer:",
    layout="wide"
)

st.title("LIGA AGALU")
st.subheader("A MAIOR LIGA DE FUTEBOL AMADOR DE RECIFE, venha fazer parte")
st.markdown("**Iniciada em 2022**")
st.markdown("Toda quinta às 20h no PSG.")

st.write("""
## Bem-vindo(a)!

Use o menu no topo (ou lateral) para navegar entre as páginas:

- **Cadastro de Jogadores**: inserir e listar os jogadores.
- **Rodadas e Jogos**: criar/editar rodadas (Times A/B/C/D) e registrar partidas (gols e assistências).
- **Dashboard**: visualizar estatísticas (jogadores, artilharia, assistências, vitórias etc.).
""")

st.markdown("---")
st.markdown("Desenvolvido com Streamlit & Firebase Firestore. Agalu 2022 ®️")
