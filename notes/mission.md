# 🏗️ Project Milestone: From CLI to Full-Stack Hangman

## 🎯 The Goal
Convert a Python-based Hangman game into a full-stack application using **MongoDB Atlas** for data persistence and **Streamlit/FastAPI** for the interface.

## 📍 Current Status
* **Environment:** macOS, Python 3.13, Virtual Environment `myvenv` active.
* **Database:** MongoDB Atlas connection tested via `pymongo` and `python-dotenv`.
* **Logic:** Functional CLI Hangman game with dictionary-based word management.

## 🗺️ The 3-Step Roadmap

1. **Data Migration:** Replace the `words = {}` dictionary with a MongoDB `DatabaseManager` that supports dynamic categories.
2. **Streamlit MVP:** Create a basic web-based "Admin Dashboard" to Add/Edit/Delete words and categories.
3. **The "Extra Mile" UI:** Use FastAPI/Flask with HTML/CSS to build a visual game with animations.

---

## ⚡ The Master Prompt (Copy & Paste this tomorrow)

> **Context:** I am working on a Python Bootcamp project. We are building a "Hangman Game" with a MongoDB Atlas backend.
>
> **What I have so far:**
> * A working CLI Hangman game that uses a local dictionary for categories (fruits, animals, countries).
> * A configured virtual environment (`myvenv`) with `pymongo` and `python-dotenv` installed.
> * A working connection to MongoDB Atlas.
>
> **The Goal for this session:** > I want to complete **Milestone 1: Data Migration**. Please help me rewrite my `manage_words` and `play_hangman` functions to use a MongoDB collection instead of the local dictionary.
>
> **Specific requirements from my instructor:**
> 1. The database must allow users to add **new** categories (not just words to existing ones).
> 2. I need a `get_random_word(category)` function that uses MongoDB's `$sample` to pull a random word.
> 3. Ensure I am using my `DatabaseManager` class structure.
>
> **Next Step after this:** We will move to Streamlit for the frontend. Please guide me through Step 1 first.

---

## 🚀 A Final Suggestion for the "Extra Mile"
When starting the HTML/CSS phase, consider using an **SVG-based Hangman**. Instead of drawing with text like `|  O`, you can hide/show parts of a digital drawing. This looks incredibly professional and counts as a massive "Extra Mile" in bootcamps.

**Status:** Ready to start Milestone 1.