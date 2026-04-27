import streamlit as st
import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")

# --- 1. PERSIST THE CLIENT ---
if "supabase_client" not in st.session_state:
    st.session_state.supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = st.session_state.supabase_client

st.set_page_config(page_title="Hangman Pro", page_icon="🎮", layout="wide")

# --- 2. AUTHENTICATION LOGIC ---

def get_current_session():
    try:
        return supabase.auth.get_session().session
    except:
        return None

current_session = get_current_session()
auth_code = st.query_params.get("code")

# THE HANDSHAKE: Only exchange the code if we are NOT logged in yet
if not current_session and auth_code:
    try:
        supabase.auth.exchange_code_for_session({"auth_code": auth_code})
        st.query_params.clear()
        st.rerun()
    except Exception as e:
        st.error(f"Handshake failed: {e}")
        if st.button("Start Fresh Login"):
            st.query_params.clear()
            st.rerun()
        st.stop()

# --- 3. MAIN ROUTING ---

if not current_session:
    st.title("🕹️ Hangman Pro")
    st.write("Please sign in with Google to start playing.")
    
    # We ONLY generate the OAuth URL if the user hasn't arrived with a code yet
    # This prevents 'Verifier Overwrite'
    if not auth_code:
        auth_response = supabase.auth.sign_in_with_oauth({
            "provider": "google",
            "options": {"redirect_to": "http://localhost:8501"}
        })
        st.link_button("Sign in with Google", auth_response.url, type="primary")
    else:
        st.info("Finishing authentication...")

else:
    # --- AUTHORIZED ZONE ---
    user_data = supabase.auth.get_user(current_session.access_token)
    profile = supabase.table("profiles").select("username, role").eq("id", user_data.user.id).single().execute()
    
    player_name = profile.data['username']
    player_role = profile.data['role']

    st.sidebar.success(f"Logged in: {player_name}")
    st.sidebar.write(f"Account: **{player_role.upper()}**")
    
    if st.sidebar.button("Logout"):
        supabase.auth.sign_out()
        st.rerun()

    # Define menu based on the 'admin' role you set in Supabase
    menu = ["Play Game", "Leaderboard"]
    if player_role in ['admin', 'super_admin']:
        menu.append("Admin Dashboard")
        
    choice = st.sidebar.selectbox("Go To", menu)

    if choice == "Admin Dashboard":
        st.header("🛡️ Admin Dashboard")
        st.success("Access Granted: Administrator Mode")
        # Add your CRUD logic here next!