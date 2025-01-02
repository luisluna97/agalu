import streamlit as st
from firestore_connection import db
import datetime

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

def criar_rodada(numero, data_rodada, timeA_ids, timeB_ids, timeC_ids, timeD_ids, goleiro1, goleiro2):
    doc_ref = db.collection("rodadas").document(str(numero))
    doc_ref.set({
        "numero": numero,
        "data_rodada": data_rodada.isoformat(),
        "timeA": timeA_ids,
        "timeB": timeB_ids,
        "timeC": timeC_ids,
        "timeD": timeD_ids,
        "goleiro1": goleiro1,
        "goleiro2": goleiro2,
        "games": []
    })
    st.success(f"Rodada {numero} salva com sucesso!")

def registrar_jogo(rodada_id, lado1_time, lado2_time, gol_lado1, gol_lado2, lista_gols, lista_assist):
    doc_ref = db.collection("games").document()
    data_jogo = {
        "rodada_id": str(rodada_id),
        "lado1_time": lado1_time,  # "A", "B", "C", "D"
        "lado2_time": lado2_time,  # "A", "B", "C", "D"
        "gols_lado1": gol_lado1,
        "gols_lado2": gol_lado2,
        "gols_detalhes": [{"autor_id": x} for x in lista_gols],
        "assistencias": [{"autor_id": x} for x in lista_assist]
    }
    doc_ref.set(data_jogo)

    # Atualizar lista de 'games' na rodada
    rod_ref = db.collection("rodadas").document(str(rodada_id))
    snap = rod_ref.get()
    if snap.exists:
        data_rod = snap.to_dict()
        g_list = data_rod.get("games", [])
        g_list.append(doc_ref.id)
        rod_ref.update({"games": g_list})
        st.success(f"Jogo cadastrado na Rodada {rodada_id}. ID={doc_ref.id}")
    else:
        st.error("Rodada não encontrada. Crie/Atualize a rodada primeiro.")

# ---------------------------
# 1) Criar/Atualizar Rodada
# ---------------------------
st.subheader("Criar/Atualizar Rodada (Times A/B/C/D)")
col1, col2 = st.columns(2)
with col1:
    numero_rodada = st.number_input("Número da Rodada", min_value=1, step=1, value=1)
with col2:
    data_rodada = st.date_input("Data da Rodada", value=datetime.date.today())

goleiro1 = st.text_input("Goleiro 1 (ex: 'nevado')", value="nevado")
goleiro2 = st.text_input("Goleiro 2 (ex: 'perri')", value="perri")

st.write("Selecione 6 jogadores para cada time (A, B, C e D).")

players_dict = get_all_players()  # {nomeJogador: idJogador}
timeA = st.multiselect("Time A (6 jogadores)", list(players_dict.keys()), key="timeA")
timeB = st.multiselect("Time B (6 jogadores)", list(players_dict.keys()), key="timeB")
timeC = st.multiselect("Time C (6 jogadores)", list(players_dict.keys()), key="timeC")
timeD = st.multiselect("Time D (6 jogadores)", list(players_dict.keys()), key="timeD")

if st.button("Criar/Atualizar Rodada"):
    if len(timeA) != 6 or len(timeB) != 6 or len(timeC) != 6 or len(timeD) != 6:
        st.error("Cada time deve ter exatamente 6 jogadores!")
    else:
        A_ids = [players_dict[n] for n in timeA]
        B_ids = [players_dict[n] for n in timeB]
        C_ids = [players_dict[n] for n in timeC]
        D_ids = [players_dict[n] for n in timeD]
        criar_rodada(numero_rodada, data_rodada, A_ids, B_ids, C_ids, D_ids, goleiro1, goleiro2)

st.markdown("---")

# ---------------------------
# 2) Registrar Jogo
# ---------------------------
st.subheader("Registrar Partida na Rodada")

rodada_input = st.text_input("Rodada (Número)", value="1")

lado1 = st.selectbox("Lado 1 (Time)", ["A","B","C","D"])
lado2 = st.selectbox("Lado 2 (Time)", ["A","B","C","D"])
gol_lado1 = st.number_input("Gols Lado 1", min_value=0, step=1, value=0)
gol_lado2 = st.number_input("Gols Lado 2", min_value=0, step=1, value=0)

st.write("Quem fez gol? (se 'gol contra', use 'sem_autor')")
total_gols = gol_lado1 + gol_lado2
lista_gols = []
opcoes_gol = ["sem_autor"] + list(players_dict.keys())

for i in range(total_gols):
    autor = st.selectbox(f"Autor do gol #{i+1}", opcoes_gol, key=f"autor_gol_{i}")
    if autor == "sem_autor":
        lista_gols.append("sem_autor")
    else:
        lista_gols.append(players_dict[autor])

st.write("Quem deu assistência? (pode ser zero ou mais)")
qtd_assist = st.number_input("Quantidade total de assistências", min_value=0, step=1, value=0)
lista_assist = []
opcoes_assist = ["sem_assistencia"] + list(players_dict.keys())

for i in range(qtd_assist):
    autor_ass = st.selectbox(f"Autor assistência #{i+1}", opcoes_assist, key=f"autor_ass_{i}")
    if autor_ass == "sem_assistencia":
        lista_assist.append("sem_assistencia")
    else:
        lista_assist.append(players_dict[autor_ass])

if st.button("Salvar Jogo"):
    if rodada_input.strip():
        registrar_jogo(
            rodada_id=rodada_input,
            lado1_time=lado1,
            lado2_time=lado2,
            gol_lado1=gol_lado1,
            gol_lado2=gol_lado2,
            lista_gols=lista_gols,
            lista_assist=lista_assist
        )
    else:
        st.warning("Informe o número da Rodada.")

st.markdown("---")

# ---------------------------
# 3) Fechar Rodada
# ---------------------------
st.subheader("Fechar Rodada")

rodada_fechar = st.text_input("Rodada para Fechar", value="1")
if st.button("Fechar Rodada"):
    rod_ref = db.collection("rodadas").document(rodada_fechar)
    snap = rod_ref.get()
    if snap.exists:
        st.success(f"Rodada {rodada_fechar} fechada (exemplo).")
        # Aqui você poderia somar estatísticas e armazenar
    else:
        st.error("Rodada não encontrada!")
