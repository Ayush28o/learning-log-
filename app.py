import streamlit as st
from supabase import create_client
from datetime import datetime
import base64
import os

# -------- PAGE CONFIG --------
st.set_page_config(page_title="The Learning Log", layout="centered")

# -------- LOAD SECRETS --------
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
APP_PASSWORD = st.secrets["APP_PASSWORD"]

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# -------- TIME BASED BACKGROUND --------
hour = datetime.now().hour

if 5 <= hour < 12:
    gradient = "linear-gradient(135deg, #fff5f7, #fde2e4)"
elif 12 <= hour < 18:
    gradient = "linear-gradient(135deg, #fdf6f0, #e8def8)"
else:
    gradient = "linear-gradient(135deg, #2b2d42, #9f86c0)"

# -------- STYLE --------
st.markdown(f"""
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;700&display=swap" rel="stylesheet">

<style>
html, body, [class*="css"] {{
    font-family: 'Playfair Display', serif;
}}

body {{
    background: {gradient};
}}

.title {{
    text-align:center;
    font-size:42px;
    font-weight:700;
    margin-top:30px;
    animation: fadeIn 2s ease-in;
}}

.subtitle {{
    text-align:center;
    color:#6d6d6d;
    margin-bottom:30px;
    animation: fadeIn 3s ease-in;
}}

.card {{
    background:white;
    padding:20px;
    border-radius:18px;
    margin-bottom:20px;
    box-shadow:0 6px 18px rgba(0,0,0,0.05);
    animation: slideUp 0.8s ease-in;
}}

@keyframes fadeIn {{
    from {{opacity:0;}}
    to {{opacity:1;}}
}}

@keyframes slideUp {{
    from {{opacity:0; transform:translateY(20px);}}
    to {{opacity:1; transform:translateY(0);}}
}}
</style>
""", unsafe_allow_html=True)

# -------- AUTH --------
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.markdown('<div class="title">Private Journal</div>', unsafe_allow_html=True)
    password = st.text_input("Enter Password", type="password")

    if st.button("Unlock"):
        if password == APP_PASSWORD:
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("Incorrect password")
    st.stop()

# -------- MAIN PAGE --------
nickname = "Divya"

st.markdown(f'<div class="title">Welcome, {nickname}</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">This space grows slowly, like us.</div>', unsafe_allow_html=True)

st.divider()

# -------- ADD ENTRY --------
with st.expander("Add Reflection"):
    understood = st.text_area("What I understood about you")
    learned = st.text_area("What I learned about myself")
    better = st.text_area("What I’ll do better")

    if st.button("Save Entry"):
        supabase.table("entries").insert({
            "date": datetime.now().strftime("%d %B %Y"),
            "understood": understood,
            "learned": learned,
            "better": better
        }).execute()
        st.success("Saved.")
        st.rerun()

st.divider()
st.subheader("Our Journey")

entries = supabase.table("entries").select("*").order("id", desc=True).execute().data

for entry in entries:
    st.markdown(f"""
    <div class="card">
        <strong>{entry['date']}</strong><br><br>
        <b>Understood:</b><br>{entry['understood']}<br><br>
        <b>Learned:</b><br>{entry['learned']}<br><br>
        <b>Better:</b><br>{entry['better']}
    </div>
    """, unsafe_allow_html=True)
