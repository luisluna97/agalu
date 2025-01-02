import streamlit as st
from firestore_connection import db
from datetime import date

st.set_page_config(page_title="Rodadas e Jogos", layout="wide")

st.title("Gerenciar Rodadas e Jogos")

# ---------------------------
# Funções Auxiliares
# ---------------------------
def inicializar_rodada(rodada_numero):
    return {
        "numero": rodada_numero,
        "data": str(date.today()),
        "jogos": [],
        "tabela": {
            "A": {"pontos": 0, "gols_pro": 0, "gols_contra": 0},
            "B": {"pontos": 0, "gols_pro": 0, "gols_contra": 0},
            "C": {"pontos": 0, "gols_pro": 0, "gols_contra": 0},
            "D": {"pontos": 0, "gols_pro": 0, "gols_contra": 0},
        },
    }

def get_registered_players():
    docs = db.collection("players").stream()
    players = ["sem autor"]
    for doc in docs:
        players.append(doc.to_dict()["name"])
    return players

def atualizar_tabela(rodada, lado_perri, lado_neve, gols_perri, gols_neve):
    if gols_perri > gols_neve:
        rodada["tabela"][lado_perri]["pontos"] += 3
    elif gols_perri < gols_neve:
        rodada["tabela"][lado_neve]["pontos"] += 3
    else:
        rodada["tabela"][lado_perri]["pontos"] += 1
        rodada["tabela"][lado_neve]["pontos"] += 1

    rodada["tabela"][lado_perri]["gols_pro"] += gols_perri
    rodada["tabela"][lado_perri]["gols_contra"] += gols_neve
    rodada["tabela"][lado_neve]["gols_pro"] += gols_neve
    rodada["tabela"][lado_neve]["gols_contra"] += gols_perri

def salvar_rodada(rodada):
    doc_ref = db.collection("rodadas").document(str(rodada["numero"]))
    doc_ref.set(rodada)
    st.success(f"Rodada {rodada['numero']} salva com sucesso!")

# ---------------------------
# Configuração de Estado
# ---------------------------
if "rodada" not in st.session_state:
    st.session_state.rodada = inicializar_rodada(1)

if "gols_perri" not in st.session_state:
    st.session_state.gols_perri = 0
if "gols_neve" not in st.session_state:
    st.session_state.gols_neve = 0
if "detalhes_gols" not in st.session_state:
    st.session_state.detalhes_gols = []

rodada = st.session_state.rodada
st.subheader(f"Rodada {rodada['numero']} - {rodada['data']}")

# ---------------------------
# Seleção dos Times para o Jogo Atual
# ---------------------------
st.markdown("### Adicionar Jogo")
col1, col2 = st.columns(2)
with col1:
    lado_perri = st.selectbox("Lado Perri (Time)", ["A", "B", "C", "D"], key="lado_perri")
with col2:
    lado_neve = st.selectbox("Lado Neve (Time)", ["A", "B", "C", "D"], key="lado_neve")

# Controle do Placar
col1, col2 = st.columns(2)
with col1:
    if st.button("+1 Lado Perri"):
        st.session_state.gols_perri += 1
        st.session_state.detalhes_gols.append({"lado": "time1", "gol": None, "assistencia": None})
    if st.button("-1 Lado Perri") and st.session_state.gols_perri > 0:
        st.session_state.gols_perri -= 1
        st.session_state.detalhes_gols.pop()
with col2:
    if st.button("+1 Lado Neve"):
        st.session_state.gols_neve += 1
        st.session_state.detalhes_gols.append({"lado": "time2", "gol": None, "assistencia": None})
    if st.button("-1 Lado Neve") and st.session_state.gols_neve > 0:
        st.session_state.gols_neve -= 1
        st.session_state.detalhes_gols.pop()

st.markdown(f"#### Placar Atual: {st.session_state.gols_perri} - {st.session_state.gols_neve}")

# Seleção de Gols e Assistências
st.markdown("### Gols e Assistências")
players = get_registered_players()
for idx, gol in enumerate(st.session_state.detalhes_gols):
    st.markdown(f"Gol #{idx + 1}")
    col1, col2 = st.columns(2)
    with col1:
        jogador_gol = st.selectbox(f"Autor do Gol (#{idx + 1})", players, key=f"gol_{idx}")
        st.session_state.detalhes_gols[idx]["gol"] = jogador_gol if jogador_gol != "sem autor" else None
    with col2:
        jogador_ass = st.selectbox(f"Assistência (#{idx + 1})", players, key=f"assist_{idx}")
        st.session_state.detalhes_gols[idx]["assistencia"] = jogador_ass if jogador_ass != "sem autor" else None

# Salvar Jogo
if st.button("Salvar Jogo"):
    rodada["jogos"].append({
        "lado_perri": lado_perri,
        "lado_neve": lado_neve,
        "gols_perri": st.session_state.gols_perri,
        "gols_neve": st.session_state.gols_neve,
        "detalhes_gols": st.session_state.detalhes_gols.copy(),
    })
    atualizar_tabela(rodada, lado_perri, lado_neve, st.session_state.gols_perri, st.session_state.gols_neve)
    st.session_state.gols_perri = 0
    st.session_state.gols_neve = 0
    st.session_state.detalhes_gols = []
    st.success("Jogo salvo com sucesso!")

# Mostrar Histórico de Jogos
st.markdown("### Jogos da Rodada")
for jogo in rodada["jogos"]:
    st.markdown(f"**{jogo['lado_perri']} {jogo['gols_perri']} x {jogo['gols_neve']} {jogo['lado_neve']}**")
    for detalhe in jogo["detalhes_gols"]:
        gol = detalhe["gol"] or "sem autor"
        assist = detalhe["assistencia"] or "sem assistência"
        st.markdown(f"- Gol: {gol}, Assistência: {assist}")

# Mostrar Tabela da Rodada
st.markdown("### Tabela da Rodada")
tabela = rodada["tabela"]
for time, dados in tabela.items():
    st.markdown(f"- **Time {time}**: {dados['pontos']} pontos, {dados['gols_pro']} gols pró, {dados['gols_contra']} gols contra")

# Encerrar Rodada
if st.button("Encerrar Rodada"):
    salvar_rodada(rodada)
    st.session_state.rodada = inicializar_rodada(rodada["numero"] + 1)
    st.success("Rodada encerrada e pronta para a próxima!")
