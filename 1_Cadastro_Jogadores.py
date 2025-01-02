import streamlit as st
from firestore_connection import db
import base64

def cadastrar_jogador(nome, tipo, habilidade, foto_file):
    foto_b64 = None
    if foto_file is not None:
        foto_bytes = foto_file.getvalue()
        foto_b64 = base64.b64encode(foto_bytes).decode()
    
    doc_ref = db.collection("players").document()
    doc_ref.set({
        "name": nome,
        "tipo": tipo,
        "habilidade": habilidade,
        "foto_base64": foto_b64
    })
    st.success(f"Jogador '{nome}' cadastrado. ID={doc_ref.id}")

st.set_page_config(page_title="Cadastro de Jogadores")

st.title("Cadastro de Jogadores")

col1, col2 = st.columns(2)

with col1:
    nome = st.text_input("Nome do Jogador")
    tipo = st.selectbox("Tipo", ["mensalista", "diarista"])
    habilidade = st.slider("Habilidade (1 a 5)", 1, 5, 3)

with col2:
    foto_file = st.file_uploader("Foto (opcional)", type=["jpg","jpeg","png"])

if st.button("Cadastrar Jogador"):
    if nome.strip():
        cadastrar_jogador(nome, tipo, habilidade, foto_file)
    else:
        st.error("Nome é obrigatório!")

st.markdown("---")
st.subheader("Jogadores Cadastrados")

players = db.collection("players").stream()
for p in players:
    data = p.to_dict()
    st.write(f"- **ID**: {p.id}, **Nome**: {data['name']}, **Tipo**: {data['tipo']}, **Habilidade**: {data['habilidade']}")
