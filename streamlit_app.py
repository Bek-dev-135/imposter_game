import streamlit as st
import pandas as pd
import random
import qrcode
import io
from urllib.parse import urlencode

# Load words from CSV
words = pd.read_csv("game_words.csv")["word"].tolist()

st.title("🕵️ Imposter Game (Offline + QR Reveal Edition)")

# Step 1: Player setup
num_players = st.number_input("👥 Number of players", min_value=3, max_value=10, step=1)
player_names = []
for i in range(int(num_players)):
    name = st.text_input(f"Enter name for Player {i+1}", f"Player {i+1}")
    player_names.append(name)

if st.button("Start Game"):
    # Step 2: Choose random word + imposter
    secret_word = random.choice(words)
    imposter_index = random.randint(0, num_players - 1)

    st.session_state["secret_word"] = secret_word
    st.session_state["imposter_index"] = imposter_index
    st.session_state["players"] = player_names

    st.success(f"Game started! Each player can scan their QR code below.")

    # Step 3: Generate QR for each player
    for i, name in enumerate(player_names):
        # Prepare individual word reveal link
        role = "Imposter" if i == imposter_index else secret_word
        qr_img = qrcode.make(role)
        
        buf = io.BytesIO()
        qr_img.save(buf, format="PNG")

        st.subheader(name)
        # Updated caption to explain the direct scan feature
        st.image(
            buf.getvalue(), 
            caption="Scan QR to see your word/role instantly", 
            use_container_width=False
        )

# Step 4: Reveal page (if link scanned)
query_params = st.query_params
if "word" in query_params:
    st.markdown("---")
    st.header(f"👋 Hi, {query_params.get('name', 'Player')}!")
    st.subheader("Your secret word:")
    st.markdown(f"### 🧩 **{query_params['word']}**")
    st.info("Don't show this to anyone!")
