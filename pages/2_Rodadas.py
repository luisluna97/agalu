import streamlit as st
from firestore_connection import db
from datetime import date

st.set_page_config(page_title="Rodadas e Jogos")

st.title("Gerenciar Rodadas e Jogos")

# ---------------------------
# Funções Auxiliares
# ---------------------------
def get_all_players():
    docs = db.collection("players").stream()
    players_dict = {}
    for d in docs:
        pd = d.to_dict()
        players_dict[pd['name']] = d.id
    return players_dict

def registrar_jogo(rodada_id, time1, time2, gols_time1, gols_time2, detalhes_gols):
    doc_ref = db.collection("games").document()
    data_jogo = {
        "rodada_id": rodada_id,
        "time1": time1,
        "time2": time2,
        "gols_time1": gols_time1,
        "gols_time2": gols_time2,
        "detalhes_gols": detalhes_gols
    }
    doc_ref.set(data_jogo)
    st.success(f"Jogo salvo com sucesso! ID: {doc_ref.id}")

# ---------------------------
# Interface para Registro
# ---------------------------
st.subheader("Registrar Partida")

rodada_id = st.text_input("Rodada (Número)", value="1")

col1, col2 = st.columns(2)
with col1:
    time1 = st.selectbox("Lado 1 (Time)", ["A", "B", "C", "D"])
with col2:
    time2 = st.selectbox("Lado 2 (Time)", ["A", "B", "C", "D"])

# Inicializar placar e detalhes
if "gols_time1" not in st.session_state:
    st.session_state.gols_time1 = 0
if "gols_time2" not in st.session_state:
    st.session_state.gols_time2 = 0
if "detalhes_gols" not in st.session_state:
    st.session_state.detalhes_gols = []

# Exibir placar
st.markdown(f"### Placar: {st.session_state.gols_time1} - {st.session_state.gols_time2}")

# Listar jogadores disponíveis
players_dict = get_all_players()
opcoes_jogadores = ["sem autor"] + list(players_dict.keys())

# Botões para adicionar gols
col1, col2 = st.columns(2)
with col1:
    if st.button("Adicionar Gol (Lado 1)"):
        st.session_state.gols_time1 += 1
        st.session_state.detalhes_gols.append({
            "lado": "time1",
            "gol": None,
            "assistencia": None
        })
with col2:
    if st.button("Adicionar Gol (Lado 2)"):
        st.session_state.gols_time2 += 1
        st.session_state.detalhes_gols.append({
            "lado": "time2",
            "gol": None,
            "assistencia": None
        })

# Preencher detalhes dos gols
for idx, gol in enumerate(st.session_state.detalhes_gols):
    st.markdown(f"### Gol #{idx + 1}")
    col1, col2 = st.columns(2)
    with col1:
        jogador_gol = st.selectbox(f"Autor do Gol (Gol #{idx + 1})", opcoes_jogadores, key=f"gol_{idx}")
        st.session_state.detalhes_gols[idx]["gol"] = jogador_gol if jogador_gol != "sem autor" else None
    with col2:
        jogador_ass = st.selectbox(f"Assistência (Gol #{idx + 1})", opcoes_jogadores, key=f"assist_{idx}")
        st.session_state.detalhes_gols[idx]["assistencia"] = jogador_ass if jogador_ass != "sem autor" else None

# Botão para salvar o jogo
if st.button("Salvar Jogo"):
    if rodada_id.strip():
        registrar_jogo(
            rodada_id=rodada_id,
            time1=time1,
            time2=time2,
            gols_time1=st.session_state.gols_time1,
            gols_time2=st.session_state.gols_time2,
            detalhes_gols=st.session_state.detalhes_gols
        )
        # Resetar o estado
        st.session_state.gols_time1 = 0
        st.session_state.gols_time2 = 0
        st.session_state.detalhes_gols = []
    else:
        st.warning("Por favor, insira o número da rodada!")
