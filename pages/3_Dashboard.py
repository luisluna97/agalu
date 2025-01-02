import streamlit as st
from firestore_connection import db
import plotly.express as px

st.set_page_config(page_title="Dashboard")

st.title("Dashboard (Estatísticas)")

# Funções Auxiliares
def get_all_games():
    docs = db.collection("games").stream()
    return [d.to_dict() for d in docs]

def get_player_name(player_id):
    # Carrega doc do "players/<player_id>"
    doc_ref = db.collection("players").document(player_id)
    snap = doc_ref.get()
    if snap.exists:
        return snap.to_dict().get("name", player_id)
    return player_id

games_data = get_all_games()

# Dicionários para contagem
gols_por_jogador = {}
assist_por_jogador = {}

for g in games_data:
    # Somar gols
    for gol in g.get("gols_detalhes", []):
        autor_id = gol["autor_id"]
        if autor_id not in ["sem_autor", None]:
            gols_por_jogador[autor_id] = gols_por_jogador.get(autor_id, 0) + 1

    # Somar assist
    for ast in g.get("assistencias", []):
        autor_id = ast["autor_id"]
        if autor_id not in ["sem_assistencia", None]:
            assist_por_jogador[autor_id] = assist_por_jogador.get(autor_id, 0) + 1

# Transformar em lista ordenada
gols_rank = sorted(gols_por_jogador.items(), key=lambda x: x[1], reverse=True)
assist_rank = sorted(assist_por_jogador.items(), key=lambda x: x[1], reverse=True)

st.subheader("Top 5 Artilheiros")
for i, (pid, val) in enumerate(gols_rank[:5], start=1):
    st.write(f"{i}. {get_player_name(pid)} - {val} gols")

st.subheader("Top 5 Assistências")
for i, (pid, val) in enumerate(assist_rank[:5], start=1):
    st.write(f"{i}. {get_player_name(pid)} - {val} assistências")

# Exemplo de gráfico de distribuição de gols
if gols_rank:
    # Pegar top 10 para gráfico
    top_gols_10 = gols_rank[:10]
    names = [get_player_name(x[0]) for x in top_gols_10]
    values = [x[1] for x in top_gols_10]
    import plotly.express as px
    fig = px.bar(
        x=names,
        y=values,
        labels={"x": "Jogador", "y": "Gols"},
        title="Top 10 Artilheiros (Geral)"
    )
    st.plotly_chart(fig, use_container_width=True)
