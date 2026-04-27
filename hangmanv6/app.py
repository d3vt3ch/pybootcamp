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
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_role' not in st.session_state:
    st.session_state.user_role = None
if 'username' not in st.session_state:
    st.session_state.username = ""

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
if 'hint' not in st.session_state:
    st.session_state.hint = ""

if 'win_recorded' not in st.session_state:
    st.session_state.win_recorded = False

# Fetch category name
if 'category_name' not in st.session_state:  
    st.session_state.category_name = ""

# --- HELPER FUNCTIONS ---
def fetch_categories():
    try:
        response = requests.get(f"{API_BASE_URL}/categories/")
        if response.status_code == 200:
            return response.json()
    except:
        return []
    return []

def start_game(player_name, category_id, category_name):
    # Fetch random word from the new endpoint
    response = requests.get(f"{API_BASE_URL}/game/word/{category_id}")
    if response.status_code == 200:
        st.session_state.chosen_word = response.json()["word"].lower()
        st.session_state.player_name = player_name
        st.session_state.game_active = True
        st.session_state.lives = 6
        st.session_state.guessed_letters = set()
        st.session_state.category_name = category_name # update category name
        st.session_state.hint = response.json()["hint"] # update hint
        st.session_state.win_recorded = False  # Reset for the new word
        st.session_state.game_active = True
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

# LOGIN / REGISTER SYSTEM
if not st.session_state.logged_in:
    st.sidebar.title("🔐 Authentication")
    auth_mode = st.sidebar.radio("Choose Mode", ["Login", "Register"])

    if auth_mode == "Register":
        st.title("📝 Create Account")
        # Wrap everything in a form
        with st.form("register_form", clear_on_submit=True):

            reg_user = st.text_input("Username")
            reg_email = st.text_input("Email")
            reg_pass = st.text_input("Password", type="password")

            # Use form_submit_button instead of st.button
            submit_reg = st.form_submit_button("Register")

            if submit_reg:
                if reg_user and reg_email and reg_pass:
                    payload = {"username": reg_user, "email": reg_email, "password": reg_pass}
                    try:
                        res = requests.post(f"{API_BASE_URL}/auth/register", json=payload)
                        if res.status_code == 200:
                            st.success("Registration successful! Switch to Login.")
                        else:
                            st.error(res.json().get("detail", "Registration failed"))
                    except Exception as e:
                        st.error(f"Connection failed: {e}")
                else:
                    st.warning("Please fill in all fields.")


    else:
        st.title("👋 Welcome Back")

        # Wrap the login inputs in a form
        with st.form("login_form"):
            log_user = st.text_input("Username")
            log_pass = st.text_input("Password", type="password")

            # This button now listens for the 'Enter' key automatically
            submit_log = st.form_submit_button("Login")

            if submit_log:
                if log_user and log_pass:
                    try:
                        res = requests.post(f"{API_BASE_URL}/auth/login", json={"username": log_user, "password": log_pass})
                        if res.status_code == 200:
                            data = res.json()
                            st.session_state.logged_in = True
                            st.session_state.username = data["username"]
                            st.session_state.user_role = data["role"]
                            st.session_state.player_name = data["username"]
                            st.rerun()
                        else:
                            st.error("Invalid credentials")
                    except Exception as e:
                        st.error(f"Server unreachable: {e}")
                else:
                    st.warning("Please enter both username and password.")
    
    st.stop() # Stops the rest of the app from loading if not logged in

# LOGGED IN NAVIGATION
st.sidebar.title(f"👤 {st.session_state.username} ({st.session_state.user_role})")
if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.user_role = None
    st.rerun()

st.sidebar.markdown("---")

st.sidebar.title("🎮 Main Menu")

# Dynamically build the menu based on roles
menu_options = ["Play Hangman", "Leaderboard"]
if st.session_state.user_role == "admin":
    menu_options.append("Manage Data")

page = st.sidebar.radio("Go to", menu_options)

#page = st.sidebar.radio("Go to", ["Play Hangman", "Leaderboard", "Manage Data"])

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
                    start_game(player_name, cat_options[selected_cat_name], selected_cat_name)
                    st.rerun()
        else:
            st.warning("No categories found. Please add some in 'Manage Data' or ensure backend is running.")

    # ACTIVE GAME LOOP
    else:
        st.markdown(
            f"""
            <div style='text-align: center; padding: 10px; font-size: 20px;'>
            🎯 The word in category: <span style='color: #00c4ff; font-weight: bold;'>{st.session_state.category_name}</span>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.markdown(
            f"<p style='text-align:center; font-size:18px;'>💡 Hint: {st.session_state.hint}</p>",
            unsafe_allow_html=True
        )

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
            if not st.session_state.win_recorded:
                record_win(st.session_state.player_name)
                st.session_state.win_recorded = True # Lock the switch
                st.balloons()
            
            if st.button("Play Again"):
                st.session_state.game_active = False
                st.session_state.win_recorded = False # Prepare for next game
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
    # Security Gate: Double-check role
    if st.session_state.user_role != "admin":
        st.error("🚫 Access Denied: You do not have permission to manage the database.")
        st.stop()
        
    st.title("⚙️ Manage Data")
    # Added a third tab for User Management
    tab1, tab2, tab3, tab4 = st.tabs(["Categories", "Words", "User Permissions","Leaderboard Tools"])
    
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
        
        st.subheader("Add New Word")
        categories = fetch_categories()
        if categories:
            cat_options = {c["name"].capitalize(): c["id"] for c in categories}
            selected_cat = st.selectbox("Select Category", list(cat_options.keys()))
            
            new_word = st.text_input("Word")
            new_hint = st.text_input("Hint")

            if st.button("Add Word"):
                res = requests.post(
                    f"{API_BASE_URL}/words/",
                    json={
                        "category_id": cat_options[selected_cat],
                        "word": new_word,
                        "hint": new_hint
                    }
                )

                if res.status_code == 200:
                    st.success("Word added successfully!")
                    st.rerun()
                else:
                    st.error("Failed to add word")
        
        st.subheader("Current Words")
        try:
            res = requests.get(f"{API_BASE_URL}/words/")
            
            if res.status_code == 200:
                data = res.json()
                for cat in data:
                    st.subheader(cat["category_name"].capitalize())
                    for w in cat["words"]:
                        st.write(f"• {w['word']} → 💡 {w['hint']}")
                
                
        except:
            st.error("Could not fetch words.")

    with tab3:
        st.subheader("👥 Account Management")
        
        res = requests.get(f"{API_BASE_URL}/auth/accounts")
        sa_res = requests.get(f"{API_BASE_URL}/auth/super-admin")
        
        if res.status_code == 200 and sa_res.status_code == 200:
            accounts = res.json()
            super_admin = sa_res.json()["username"]
            
            st.dataframe(accounts, use_container_width=True, hide_index=True)
            st.divider()
            
            st.subheader("🛠️ User Actions")
            other_users = [a["username"] for a in accounts if a["username"] != st.session_state.username]

            if other_users:
                selected_user = st.selectbox("Select a User to Manage:", other_users)
                current_role = next(item["role"] for item in accounts if item["username"] == selected_user)

                # --- PROTECTION CHECK ---
                if selected_user == super_admin:
                    st.info(f"🛡️ **{selected_user}** is the Super Admin (Creator). Access to demote or delete this account is restricted.")

                    # Only allow password reset (helpful if the Super Admin forgets theirs)
                    new_password = st.text_input("Reset Super Admin Password", type="password")
                    if st.button("Force Reset"):
                        # ... reset logic ...
                        pass

                else:
                    # Show the normal Promote/Demote/Delete buttons for everyone else
                    col1, col2, col3 = st.columns(3)

                    with col1:
                    # Show Promote button only if they are a player
                        if current_role == "player":
                            if st.button("🚀 Promote to Admin", use_container_width=True):
                                res = requests.put(f"{API_BASE_URL}/auth/promote/{selected_user}")
                                st.success(f"{selected_user} promoted!")
                                st.rerun()
                        # Show Demote button only if they are an admin
                        else:
                            if st.button("📉 Demote to Player", use_container_width=True):
                                res = requests.put(f"{API_BASE_URL}/auth/demote/{selected_user}")
                                st.warning(f"{selected_user} demoted.")
                                st.rerun()

                    with col2:
                        # Danger Zone: Delete Account
                        if st.button("🗑️ Delete Account", type="secondary", use_container_width=True):
                            # Simple confirmation check
                            st.session_state.confirm_delete = selected_user
                    
                    # Confirmation logic for deletion
                    if 'confirm_delete' in st.session_state and st.session_state.confirm_delete == selected_user:
                        st.warning(f"Are you sure you want to permanently delete {selected_user}?")
                        if st.button(f"Yes, Delete {selected_user} Permanently"):
                            del_res = requests.delete(f"{API_BASE_URL}/auth/accounts/{selected_user}")
                            if del_res.status_code == 200:
                                st.success("Account deleted.")
                                del st.session_state.confirm_delete
                                st.rerun()
                    
                    # Inside your 'with tab3:' block, under 'col3'
                    with col3:
                        st.write("🔑 **Security**")
                        new_password = st.text_input("New Password", type="password", key=f"pwd_{selected_user}")
                        if st.button("Reset Password", use_container_width=True):
                            if new_password:
                                reset_res = requests.put(
                                    f"{API_BASE_URL}/auth/reset-password/{selected_user}",
                                    json={"username": selected_user, "password": new_password}
                                )
                                if reset_res.status_code == 200:
                                    st.success(f"Password reset for {selected_user}!")
                                else:
                                    st.error("Reset failed.")
                            else:
                                st.warning("Enter a new password first.")
            else:
                st.info("No other users found.")
                
        else:
            st.error("Could not fetch account list.")

    with tab4:
        st.subheader("🏆 Leaderboard Management")
        st.info("Use this section to manage the public scoreboard. Be careful: these actions are permanent.")
        
        st.divider()
        
        st.write("### Danger Zone")
        # Creating a confirmation flow for resetting scores
        if "confirm_reset" not in st.session_state:
            st.session_state.confirm_reset = False

        if not st.session_state.confirm_reset:
            if st.button("🚨 Reset Entire Scoreboard", type="primary", use_container_width=True):
                st.session_state.confirm_reset = True
                st.rerun()
        else:
            st.warning("⚠️ Are you absolutely sure? This will delete all player wins forever.")
            col_yes, col_no = st.columns(2)
            
            with col_yes:
                if st.button("Yes, Clear Everything", type="primary", use_container_width=True):
                    res = requests.delete(f"{API_BASE_URL}/game/reset-scores")
                    if res.status_code == 200:
                        st.success("The scoreboard is now clean!")
                        st.session_state.confirm_reset = False
                        st.balloons() # A little celebration for a fresh start
                        st.rerun()
            
            with col_no:
                if st.button("Cancel", use_container_width=True):
                    st.session_state.confirm_reset = False
                    st.rerun()