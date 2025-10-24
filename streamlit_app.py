import streamlit as st
import pandas as pd
import random

# -----------------------
# Load data
# -----------------------
@st.cache_data
def load_words():
    df = pd.read_csv("game_words.csv")
    topics = df.groupby("topic")["word"].apply(list).to_dict()
    return topics

topics = load_words()

# -----------------------
# App title and intro
# -----------------------
st.set_page_config(page_title="Imposter Game", page_icon="🎭", layout="centered")
st.title("🎭 Imposter Game (Offline Edition)")
st.write("Welcome to the offline Imposter Game! No AI, just fun logic and bluffing.")

# -----------------------
# Player setup
# -----------------------
players = st.number_input("👥 Number of players:", min_value=3, max_value=10, value=4)
names = []
for i in range(players):
    name = st.text_input(f"Enter name for Player {i+1}", f"Player {i+1}")
    names.append(name)

# -----------------------
# Game setup
# -----------------------
if st.button("🎲 Start Game"):
    topic = random.choice(list(topics.keys()))
    word = random.choice(topics[topic])
    imposter_index = random.randint(0, players - 1)

    st.session_state["topic"] = topic
    st.session_state["word"] = word
    st.session_state["imposter_index"] = imposter_index
    st.session_state["names"] = names
    st.session_state["assigned"] = [False] * players
    st.experimental_rerun()

# -----------------------
# Role assignment phase
# -----------------------
if "topic" in st.session_state and not all(st.session_state["assigned"]):
    st.subheader("🔐 Role Assignment")

    topic = st.session_state["topic"]
    word = st.session_state["word"]
    imposter_index = st.session_state["imposter_index"]
    names = st.session_state["names"]

    for i, name in enumerate(names):
        if not st.session_state["assigned"][i]:
            if st.button(f"Reveal word for {name}"):
                if i == imposter_index:
                    st.warning(f"{name}, you are the IMPOSTER! 🤫 You don’t know the word. Pretend you do.")
                else:
                    st.success(f"{name}, the secret word is: **{word}**")
                st.session_state["assigned"][i] = True
                st.stop()  # show only one player’s word at a time

# -----------------------
# Discussion and voting phase
# -----------------------
if "topic" in st.session_state and all(st.session_state["assigned"]):
    st.subheader("💬 Discussion Time!")
    st.info(f"Topic: **{st.session_state['topic']}**")

    st.write("Now discuss and figure out who the imposter might be.")
    st.write("When ready, cast your votes below.")

    vote = st.selectbox("Vote for who you think is the imposter:", st.session_state["names"])
    if st.button("🗳️ Submit Vote"):
        st.session_state["vote"] = vote
        st.success(f"You voted for {vote}. Waiting for others...")

    if st.button("🔎 Reveal Imposter"):
        imposter_name = st.session_state["names"][st.session_state["imposter_index"]]
        word = st.session_state["word"]
        st.error(f"😈 The Imposter was **{imposter_name}**!")
        st.info(f"The secret word was: **{word}**")

        if st.session_state.get("vote") == imposter_name:
            st.success("🎉 You caught the imposter! Great job!")
        else:
            st.warning("🙈 The imposter fooled you this time!")

        if st.button("🔁 Play Again"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.experimental_rerun()
