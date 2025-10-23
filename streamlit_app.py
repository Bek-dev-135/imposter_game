import streamlit as st
import random
import uuid
import io
import qrcode
from openai import OpenAI

# --- API KEY ROTATION ---
keys = st.secrets["OPENAI_KEYS"]

def get_valid_client():
    for key in keys:
        client = OpenAI(api_key=key)
        try:
            client.models.list()
            return client
        except Exception as e:
            print(f"Key failed: {key[:8]}... {e}")
    raise Exception("All API keys failed")

client = get_valid_client()

# --- STREAMLIT APP ---
st.title("🎭 Imposter Game")

if "games" not in st.session_state:
    st.session_state.games = {}

# --- HOST SECTION ---
st.header("Host a Game")
num_players = st.number_input("Number of players", min_value=4, max_value=20, value=4)

if st.button("Start Game"):
    game_id = str(uuid.uuid4())[:8]
    main_word = random.choice(["Beach", "Pizza", "Movie", "Cat", "Airport"])

    hint_word = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Generate a vague but related hint word."},
            {"role": "user", "content": f"Main word: {main_word}"}
        ]
    ).choices[0].message.content.strip()

    players = list(range(1, num_players + 1))
    num_imposters = max(1, num_players // 4)
    imposters = random.sample(players, num_imposters)

    st.session_state.games[game_id] = {
        "main_word": main_word,
        "hint_word": hint_word,
        "players": [
            {"id": i, "role": "imposter" if i in imposters else "normal"} for i in players
        ]
    }

    st.success(f"Game created! ID: {game_id}")
    st.write(f"**Main Word:** {main_word}")
    st.write(f"**Hint Word (for imposters):** {hint_word}")

    st.write("📱 Scan your QR code to join:")
    for p in st.session_state.games[game_id]["players"]:
        player_url = f"{st.request.host_url}?game={game_id}&player={p['id']}"
        buf = io.BytesIO()
        qrcode.make(player_url).save(buf)
        st.image(buf.getvalue(), caption=f"Player {p['id']}")

# --- PLAYER VIEW ---
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
