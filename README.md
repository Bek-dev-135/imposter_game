🕵️ Imposter Game (Streamlit QR Reveal)

A local-multiplayer social deduction game built with Streamlit. It uses dynamically generated QR codes to reveal secret roles to players on their personal devices, all from a single application screen.

This app is a simple way to play a "Spyfall" or "Among Us" style party game using a single laptop or tablet as the host.

🚀 How to Play

Host: One person runs the Streamlit app on a laptop or tablet by visiting this link https://imposter-game.streamlit.app/

Setup: Enter the number of players (3-10) and their names.

Start: Click "Start Game." The app will display a unique QR code for each player.

Scan: Each player, in turn, scans only their own QR code using their phone's camera.

Reveal:

Players will see a message like: Your secret word is: Coffee

The Imposter will see: You are the Imposter! 🤫 Impersonate the role. The topic is: Coffee

Discuss: All players (including the imposter) discuss the topic, trying to figure out who doesn't know the secret word.

Vote: Once ready, players cast their vote for who they think the imposter is.

Win: Click "Reveal Imposter" to see if the players successfully caught the imposter or if the imposter fooled everyone!

✨ Features

Local Multiplayer: Play with 3-10 players on a single shared screen.

Private Role Reveal: Uses dynamically generated QR codes for a "no-link, no-internet" private reveal.

Anti-Metagaming: All QR codes are programmatically forced to the exact same pixel dimensions (using qrcode.QRCode(version=4)). This prevents players from identifying the imposter based on a larger, more complex QR code.

Simple Game Flow: Entire game (setup, reveal, vote, and reset) is managed in a single Streamlit app using st.session_state.

🛠️ Installation & Running

Clone the repository:

git clone [https://github.com/your-username/imposter-game.git](https://github.com/your-username/imposter-game.git)
cd imposter-game


Install dependencies:
It's recommended to use a virtual environment.

python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
pip install -r requirements.txt


Create your word list:
The app requires a game_words.csv file in the same directory. Create this file with a single column header named word.

game_words.csv example:

word
Coffee
Dog
Laptop
Mountain
Telescope
Guitar
Pizza
Ocean


Run the app:

streamlit run imposter_game.py


Your browser will automatically open to the game.

🗂️ File Structure

.
├── imposter_game.py     # The main Streamlit application
├── game_words.csv       # (You must create this) The list of secret words
├── requirements.txt     # Python dependencies
└── README.md            # You are here!
