import os
import random
from fastapi import FastAPI, HTTPException
from supabase import create_client, Client
from dotenv import load_dotenv

# --- INITIAL SETUP ---
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY") 

# Pure FastAPI connection
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI(title="Hangman Pro: Backend Engine")

@app.get("/")
def health_check():
    return {"status": "Backend is active and ready"}

@app.get("/categories/")
def fetch_categories():
    response = supabase.table("categories").select("*").execute()
    return response.data

@app.get("/game/random-word/{category_id}")
def get_word(category_id: int):
    query = supabase.table("words").select("word, hint").eq("category_id", category_id).execute()
    if not query.data:
        raise HTTPException(status_code=404, detail="No words found")
    return random.choice(query.data)