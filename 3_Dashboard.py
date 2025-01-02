import streamlit as st
from firestore_connection import db
import plotly.express as px

st.set_page_config(page_title="Dashboard")

st.title("Dashboard Liga Agalu")

# Exemplo: Contar quantos jogadores são mensalistas vs diaristas
players_ref = db.collection("players").stream()
mensal = 0
diar = 0
for doc in players_ref:
    tipo = doc.to_dict().get("tipo")
    if tipo == "mensalista":
        mensal += 1
    else:
        diar += 1

col1, col2 = st.columns(2)
with col1:
    st.metric(label="Total Mensalistas", value=mensal)
    st.metric(label="Total Diaristas", value=diar)

with col2:
    fig = px.bar(x=["Mensalistas", "Diaristas"], y=[mensal, diar],
                 labels={"x": "Tipo", "y": "Quantidade"},
                 title="Distribuição de Jogadores")
    st.plotly_chart(fig, use_container_width=True)

# Podem vir aqui outros gráficos: artilharia, aproveitamento, etc.
st.markdown("---")
st.subheader("Estatísticas de Partidas (Exemplo)")

# Contar quantos jogos temos:
games_ref = db.collection("games").stream()
count_games = 0
total_gols = 0
for g in games_ref:
    data = g.to_dict()
    count_games += 1
    total_gols += data.get("goals_sideA", 0) + data.get("goals_sideB", 0)

st.write(f"- **Partidas Registradas**: {count_games}")
st.write(f"- **Total de Gols**: {total_gols}")

if count_games > 0:
    media_gols = total_gols / count_games
    st.write(f"- **Média de Gols por Partida**: {media_gols:.2f}")
