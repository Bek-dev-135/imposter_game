import streamlit as st
import pandas as pd
import random
import qrcode
import io
# from urllib.parse import urlencode # Removed: No longer needed as we encode the word directly

# Load words from CSV
# NOTE: This assumes a file named 'game_words.csv' exists in the same directory.
try:
    words = pd.read_csv("game_words.csv")["word"].tolist()
except FileNotFoundError:
    st.error("Error: 'game_words.csv' not found. Using fallback words.")
    words = ["Coffee", "Dog", "Laptop", "Mountain", "Telescope"] # Fallback words

st.title("🕵️ Imposter Game (Direct QR Reveal Edition)")

# Use st.session_state to persist data and manage flow
if "game_started" not in st.session_state:
    st.session_state["game_started"] = False
    st.session_state["num_players"] = 3
    st.session_state["players"] = []
    st.session_state["vote"] = None
    st.session_state["secret_word"] = None
    st.session_state["imposter_index"] = None
    st.session_state["topic"] = None # Initialize topic for the imposter

# Step 1: Player setup
st.session_state["num_players"] = st.number_input(
    "👥 Number of players", 
    min_value=3, 
    max_value=10, 
    step=1, 
    value=st.session_state["num_players"]
)

player_names = []
for i in range(int(st.session_state["num_players"])):
    # Key ensures the input state is stable
    name = st.text_input(f"Enter name for Player {i+1}", f"Player {i+1}", key=f"p_name_{i}")
    player_names.append(name)
    
st.session_state["players"] = player_names


if st.button("Start Game"):
    # Reset game state for a new round
    st.session_state["game_started"] = True
    st.session_state["vote"] = None # Reset vote

    # Step 2: Choose random word + imposter
    secret_word = random.choice(words)
    imposter_index = random.randint(0, st.session_state["num_players"] - 1)
    
    # Set the topic (using the word itself, framed as a generic topic for the imposter)
    topic = secret_word

    st.session_state["secret_word"] = secret_word
    st.session_state["imposter_index"] = imposter_index
    st.session_state["topic"] = topic

    st.success("Game started! Each player, scan your code below to learn your role.")
    # NOTE: The QR code generation is now moved inside the 'game_started' block below
    # This ensures it persists on screen after the button click.


# -----------------------
# Main Game Flow (Steps 3 & 4)
# -----------------------

if st.session_state["game_started"]:
    # --- THIS BLOCK WAS MOVED HERE ---
    st.subheader("🔑 Role Reveal")
    # Step 3: Generate QR for each player
    for i, name in enumerate(st.session_state["players"]):
        
        # --- MODIFIED QR CODE CONTENT (using st.session_state) ---
        if i == st.session_state["imposter_index"]:
            # Imposter gets a descriptive message revealing only the general topic
            role = f"You are the Imposter! 🤫\n\nImpersonate the role.\nThe topic is: {st.session_state['topic']}"
        else:
            # Non-Imposter gets the secret word with a descriptive phrase
            role = f"Your secret word is: {st.session_state['secret_word']}"
        # --- END MODIFIED QR CODE CONTENT ---
        
        # Generate QR code, encoding the full 'role' message directly
        qr_img = qrcode.make(role)
        
        buf = io.BytesIO()
        qr_img.save(buf, format="PNG")

        st.markdown(f"**{name}**")
        # Updated caption to explain the direct scan feature
        st.image(
            buf.getvalue(), 
            caption="Scan QR code instantly to see your secret role/word.", 
            use_container_width=False
        )
        st.markdown("---")
    # --- END MOVED BLOCK ---


    # -----------------------
    # Discussion and voting phase (New Step 4)
    # -----------------------
    
    # The QR code reveal is simultaneous, so we skip the sequential assignment phase.
    # The discussion and voting phase starts immediately after the codes are scanned.
    
    st.subheader("💬 Discussion and Voting Phase")
    
    # Display the general topic for all players to see
    st.info(f"The general topic is: **{st.session_state['topic']}**")

    st.write("Discuss the topic and observe who seems suspicious. When ready, cast your vote.")
    
    # Voting Mechanism
    if st.session_state["vote"] is None:
        vote = st.selectbox(
            "Vote for who you think is the imposter:", 
            st.session_state["players"], 
            key="current_vote_select"
        )
        
        if st.button("🗳️ Submit Vote"):
            st.session_state["vote"] = vote
            st.success(f"You voted for **{vote}**. The game is now ready for the final reveal.")
            # st.experimental_rerun() # Rerunning here can cause issues with other player states if this were multiplayer
    else:
        st.warning(f"Your vote for **{st.session_state['vote']}** has been recorded.")

    
    # Reveal Imposter Button
    st.markdown("---")
    if st.button("🔎 Reveal Imposter"):
        imposter_name = st.session_state["players"][st.session_state["imposter_index"]]
        secret_word = st.session_state["secret_word"]
        
        st.error(f"😈 The Imposter was **{imposter_name}**!")
        st.info(f"The secret word everyone else was discussing was: **{secret_word}**")

        # Check the recorded vote
        if st.session_state.get("vote") == imposter_name:
            st.balloons()
            st.success("🎉 **Success!** The players successfully caught the imposter!")
        elif st.session_state.get("vote") is None:
            st.warning("🙈 **Failure.** No vote was submitted, and the imposter was revealed.")
        else:
            st.warning(f"🙈 **Failure.** The players voted for **{st.session_state['vote']}** but the imposter was {imposter_name}. The imposter wins!")

    
    st.markdown("---")
    # Display a button to clear the game state
    if st.button("🔁 Play Again"):
        # Clear specific keys and rerun to reset the interface
        for key in list(st.session_state.keys()):
            # Keep player count and player names input state consistent
            if not key.startswith("p_name_") and key not in ["num_players", "players"]:
                del st.session_state[key]
        st.rerun()

