import streamlit as st
from firestore_connection import db
import datetime

def criar_rodada(numero, data_rodada):
    doc_ref = db.collection("rodadas").document()
    doc_ref.set({
        "numero": numero,
        "data_rodada": data_rodada.isoformat(),
        "games": []
    })
    st.success(f"Rodada {numero} criada. ID={doc_ref.id}")

def registrar_jogo(rodada_id, timeA, timeA_players, timeB, timeB_players, golA, golB, goleiroA, goleiroB):
    game_ref = db.collection("games").document()
    game_data = {
        "rodada_id": rodada_id,
        "timeA_nome": timeA,
        "timeB_nome": timeB,
        "timeA_players": timeA_players,
        "timeB_players": timeB_players,
        "goals_sideA": golA,
        "goals_sideB": golB,
        "goleiro_sideA": goleiroA,
        "goleiro_sideB": goleiroB
    }
    game_ref.set(game_data)

    rod_ref = db.collection("rodadas").document(rodada_id)
    snap = rod_ref.get()
    if snap.exists:
        data = snap.to_dict()
        lista_games = data.get("games", [])
        lista_games.append(game_ref.id)
        rod_ref.update({"games": lista_games})
        st.success(f"Jogo registrado na rodada {rodada_id}. (ID={game_ref.id})")
    else:
        st.error("Rodada não encontrada.")

st.set_page_config(page_title="Rodadas")

st.title("Gerenciar Rodadas")

# Criar rodada
st.subheader("Criar Nova Rodada")
col1, col2 = st.columns(2)

with col1:
    numero = st.number_input("Número da Rodada", min_value=1, step=1)
with col2:
    data_rodada = st.date_input("Data da Rodada", value=datetime.date.today())

if st.button("Criar Rodada"):
    criar_rodada(numero, data_rodada)

st.markdown("---")

# Registrar jogo
st.subheader("Registrar Jogo")
rodada_id = st.text_input("ID da Rodada")
timeA = st.text_input("Nome do Time A", "Time A")
timeB = st.text_input("Nome do Time B", "Time B")

goleiroA = st.text_input("Goleiro lado A", "perri")
goleiroB = st.text_input("Goleiro lado B", "nevado")

colA, colB = st.columns(2)
with colA:
    timeA_players_raw = st.text_input("IDs Jogadores Time A (sep. por vírgula)")
    golA = st.number_input("Gols Time A", min_value=0, step=1)
with colB:
    timeB_players_raw = st.text_input("IDs Jogadores Time B (sep. por vírgula)")
    golB = st.number_input("Gols Time B", min_value=0, step=1)

if st.button("Registrar Jogo"):
    if rodada_id.strip():
        tA_players = [x.strip() for x in timeA_players_raw.split(",") if x.strip()]
        tB_players = [x.strip() for x in timeB_players_raw.split(",") if x.strip()]
        registrar_jogo(rodada_id, timeA, tA_players, timeB, tB_players, golA, golB, goleiroA, goleiroB)
    else:
        st.warning("Informe o ID da Rodada.")

st.markdown("---")
st.subheader("Rodadas Existentes")

rodadas = db.collection("rodadas").stream()
for r in rodadas:
    rd = r.to_dict()
    st.write(f"**Rodada** {rd['numero']} (ID={r.id}) | Data: {rd['data_rodada']}")
    st.write(f"Jogos cadastrados: {rd.get('games',[])}")
    st.write("---")
