# Stable code during presentation

import streamlit as st
import requests
import time

# --- CONFIGURATION ---
API_BASE_URL = "http://localhost:8000"

st.set_page_config(page_title="Hangman Web", page_icon="🎮", layout="centered")

# --- HANGMAN ASCII ART ---
STAGES = [
    """
    --------
    |      |
    |      O
    |     \\|/
    |      |
    |     / \\
    -
    """,
    """
    --------
    |      |
    |      O
    |     \\|/
    |      |
    |     / 
    -
    """,
    """
    --------
    |      |
    |      O
    |     \\|/
    |      |
    |      
    -
    """,
    """
    --------
    |      |
    |      O
    |     \\|
    |      |
    |     
    -
    """,
    """
    --------
    |      |
    |      O
    |      |
    |      |
    |     
    -
    """,
    """
    --------
    |      |
    |      O
    |    
    |      
    |     
    -
    """,
    """
    --------
    |      |
    |      
    |    
    |      
    |     
    -
    """
]

# --- SESSION STATE INITIALIZATION ---
if 'game_active' not in st.session_state: # 
    st.session_state.game_active = False
if 'chosen_word' not in st.session_state:
    st.session_state.chosen_word = ""
if 'lives' not in st.session_state:
    st.session_state.lives = 6
if 'guessed_letters' not in st.session_state:
    st.session_state.guessed_letters = set()
if 'player_name' not in st.session_state:
    st.session_state.player_name = ""

# --- HELPER FUNCTIONS ---
def fetch_categories():
    try:
        response = requests.get(f"{API_BASE_URL}/categories/")
        if response.status_code == 200:
            return response.json()
    except:
        return []
    return []

def start_game(player_name, category_id):
    # Fetch random word from the new endpoint
    response = requests.get(f"{API_BASE_URL}/game/word/{category_id}")
    if response.status_code == 200:
        st.session_state.chosen_word = response.json()["word"].lower()
        st.session_state.player_name = player_name
        st.session_state.game_active = True
        st.session_state.lives = 6
        st.session_state.guessed_letters = set()
    else:
        st.error("Failed to fetch word. Category might be empty.")

def handle_guess():
    guess = st.session_state.current_guess.lower()
    if guess and guess.isalpha() and len(guess) == 1:
        if guess not in st.session_state.guessed_letters:
            st.session_state.guessed_letters.add(guess)
            if guess not in st.session_state.chosen_word:
                st.session_state.lives -= 1
    # Clear the input box after guess
    st.session_state.current_guess = ""

def record_win(player_name):
    # Use your new POST endpoint
    requests.post(f"{API_BASE_URL}/game/win", params={"player_name": player_name})


# --- MAIN UI NAVIGATION ---
st.sidebar.title("🎮 Main Menu")
page = st.sidebar.radio("Go to", ["Play Hangman", "Leaderboard", "Manage Data"])

st.sidebar.markdown("---")
#st.sidebar.info("FastAPI Backend must be running on localhost:8000")


# ==========================================
# PAGE 1: PLAY HANGMAN
# ==========================================
if page == "Play Hangman":
    st.title("Play Hangman")

    # PRE-GAME SETUP
    if not st.session_state.game_active:
        st.subheader("Game Setup")
        player_name = st.text_input("Enter your name:", value=st.session_state.player_name)
        
        categories = fetch_categories()
        if categories:
            # Create a dictionary mapping category names to their IDs for the selectbox
            cat_options = {c["name"].capitalize(): c["id"] for c in categories}
            selected_cat_name = st.selectbox("Choose a Category:", list(cat_options.keys()))
            
            if st.button("Start Game", type="primary"):
                if player_name.strip() == "":
                    st.warning("Please enter your name first!")
                else:
                    start_game(player_name, cat_options[selected_cat_name])
                    st.rerun()
        else:
            st.warning("No categories found. Please add some in 'Manage Data' or ensure backend is running.")

    # ACTIVE GAME LOOP
    else:
        st.write(f"**Player:** {st.session_state.player_name} | **Lives Left:** {st.session_state.lives}")
        
        # Display Hangman Art
        st.code(STAGES[st.session_state.lives], language="text")

        # Display Word Placeholder (e.g., a p p _ e)
        display_word = ""
        for letter in st.session_state.chosen_word:
            if letter in st.session_state.guessed_letters:
                display_word += letter + " "
            else:
                display_word += "_ "
        
        st.markdown(f"### {display_word}")
        st.write(f"**Guessed Letters:** {', '.join(sorted(st.session_state.guessed_letters))}")

        # Check Win/Loss conditions before allowing another guess
        word_is_guessed = all(letter in st.session_state.guessed_letters for letter in st.session_state.chosen_word)
        
        if st.session_state.lives == 0:
            st.error(f"Game Over! The word was: **{st.session_state.chosen_word}**")
            if st.button("Play Again"):
                st.session_state.game_active = False
                st.rerun()
                
        elif word_is_guessed:
            st.success(f"🎉 You win, {st.session_state.player_name}! 🎉")
            st.balloons()
            # Record win only once per game
            record_win(st.session_state.player_name)
            if st.button("Play Again"):
                st.session_state.game_active = False
                st.rerun()
                
        else:
            # Input for guessing
            st.text_input("Guess a letter:", max_chars=1, key="current_guess", on_change=handle_guess)
            if st.button("End Game Early"):
                st.session_state.game_active = False
                st.rerun()


# ==========================================
# PAGE 2: LEADERBOARD
# ==========================================
elif page == "Leaderboard":
    st.title("🏆 Leaderboard")
    
    try:
        response = requests.get(f"{API_BASE_URL}/users/")
        if response.status_code == 200:
            users = response.json()
            if users:
                # Streamlit automatically formats list of dicts into a nice table
                st.dataframe(users, use_container_width=True, hide_index=True)
            else:
                st.info("No scores recorded yet. Go play a game!")
    except Exception as e:
        st.error(f"Failed to connect to backend: {e}")


# ==========================================
# PAGE 3: MANAGE DATA (Basic Skeleton)
# ==========================================
elif page == "Manage Data":
    st.title("⚙️ Manage Data")
    tab1, tab2 = st.tabs(["Categories", "Words"])
    
    with tab1:
        st.subheader("Add New Category")
        new_cat = st.text_input("Category Name:")
        if st.button("Add Category"):
            res = requests.post(f"{API_BASE_URL}/categories/", json={"name": new_cat})
            if res.status_code == 200:
                st.success("Category added!")
            else:
                st.error("Failed or Category exists.")

        st.divider()
        st.subheader("Current Categories")
        cats = fetch_categories()
        if cats:
            st.table(cats)
            
    with tab2:
        st.subheader("Current Words")
        try:
            res = requests.get(f"{API_BASE_URL}/words/")
            if res.status_code == 200:
                st.json(res.json()) # Displays the complex JSON cleanly
        except:
            st.error("Could not fetch words.")