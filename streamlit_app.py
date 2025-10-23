import streamlit as st
import random, uuid, qrcode, io
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("🎭 Imposter Game")

if "games" not in st.session_state:
    st.session_state.games = {}

# Host section
st.header("Host a Game")
num_players = st.number_input("Number of players", min_value=4, max_value=20, value=4)
if st.button("Start Game"):
    game_id = str(uuid.uuid4())[:8]
    main_word = random.choice(["Beach", "Pizza", "Movie", "Cat", "Airport"])
    hint_word = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":f"Give a vague but related hint for '{main_word}'"}]
    ).choices[0].message.content.strip()

    players = list(range(1, num_players + 1))
    num_imposters = max(1, num_players // 4)
    imposters = random.sample(players, num_imposters)

    st.session_state.games[game_id] = {
        "main_word": main_word,
        "hint_word": hint_word,
        "players": [{"id": i, "role": "imposter" if i in imposters else "normal"} for i in players]
    }

    st.success(f"Game created! ID: {game_id}")

    st.write("Scan your QR code to join:")
    for p in st.session_state.games[game_id]["players"]:
        player_url = f"{st.request.host_url}?game={game_id}&player={p['id']}"
        buf = io.BytesIO()
        qrcode.make(player_url).save(buf)
        st.image(buf.getvalue(), caption=f"Player {p['id']}")

# Player View
params = st.query_params
if "game" in params and "player" in params:
    game_id = params["game"]
    pid = int(params["player"])
    game = st.session_state.games.get(game_id)
    if game:
        role = next(p["role"] for p in game["players"] if p["id"] == pid)
        word = game["hint_word"] if role == "imposter" else game["main_word"]
        st.write(f"Your word is: **{word}**")
        st.write("🤫 Don't tell anyone your word!")
