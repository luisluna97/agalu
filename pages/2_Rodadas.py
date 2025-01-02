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

# ---------------------------
# Interface para Registro
# ---------------------------
rodada = st.session_state.rodada
st.subheader(f"Rodada {rodada['numero']} - {rodada['data']}")

# Seleção dos Times para o Jogo Atual
st.markdown("### Adicionar Jogo")
col1, col2 = st.columns(2)
with col1:
    lado_perri = st.selectbox("Lado Perri (Time)", ["A", "B", "C", "D"], key="lado_perri")
with col2:
    lado_neve = st.selectbox("Lado Neve (Time)", ["A", "B", "C", "D"], key="lado_neve")

# Controle do Placar
if "gols_perri" not in st.session_state:
    st.session_state.gols_perri = 0
if "gols_neve" not in st.session_state:
    st.session_state.gols_neve = 0

col1, col2 = st.columns(2)
with col1:
    if st.button("+1 Lado Perri"):
        st.session_state.gols_perri += 1
with col2:
    if st.button("+1 Lado Neve"):
        st.session_state.gols_neve += 1

st.markdown(f"#### Placar Atual: {st.session_state.gols_perri} - {st.session_state.gols_neve}")

# Seleção de Gols e Assistências
st.markdown("### Gols e Assistências")
detalhes_gols = []
for i in range(st.session_state.gols_perri + st.session_state.gols_neve):
    st.markdown(f"Gol #{i + 1}")
    col1, col2 = st.columns(2)
    with col1:
        autor_gol = st.selectbox(f"Autor do Gol (#{i + 1})", ["sem autor"] + ["Jogador 1", "Jogador 2"], key=f"gol_{i}")
    with col2:
        assistencia = st.selectbox(f"Assistência (#{i + 1})", ["sem assistência"] + ["Jogador 1", "Jogador 2"], key=f"assist_{i}")
    detalhes_gols.append({"gol": autor_gol, "assistencia": assistencia})

# Salvar Jogo
if st.button("Salvar Jogo"):
    rodada["jogos"].append({
        "lado_perri": lado_perri,
        "lado_neve": lado_neve,
        "gols_perri": st.session_state.gols_perri,
        "gols_neve": st.session_state.gols_neve,
        "detalhes_gols": detalhes_gols,
    })
    atualizar_tabela(rodada, lado_perri, lado_neve, st.session_state.gols_perri, st.session_state.gols_neve)
    st.session_state.gols_perri = 0
    st.session_state.gols_neve = 0
    st.success("Jogo salvo com sucesso!")

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
