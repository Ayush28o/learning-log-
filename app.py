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

/* APP BACKGROUND */
[data-testid="stAppViewContainer"] {{
    background: {gradient};
    overflow: hidden;
}}

/* FADE PAGE IN */
[data-testid="stAppViewContainer"] > .main {{
    animation: pageFade 1.2s ease-in-out;
}}

@keyframes pageFade {{
    from {{opacity: 0; transform: translateY(10px);}}
    to {{opacity: 1; transform: translateY(0);}}
}}

/* FONT */
html, body, [class*="css"] {{
    font-family: 'Playfair Display', serif;
}}

/* TITLE */
.title {{
    text-align:center;
    font-size:48px;
    font-weight:700;
    margin-top:40px;
    color:#2b2d42;
    animation: fadeIn 2s ease-in;
}}

.subtitle {{
    text-align:center;
    color:#6d6875;
    margin-bottom:40px;
    animation: fadeIn 2.5s ease-in;
}}

/* CARDS */
.card {{
    background:white;
    padding:24px;
    border-radius:22px;
    margin-bottom:25px;
    box-shadow:0 12px 35px rgba(0,0,0,0.08);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    animation: slideUp 0.8s ease-in;
}}

.card:hover {{
    transform: translateY(-6px);
    box-shadow:0 20px 50px rgba(0,0,0,0.12);
}}

@keyframes slideUp {{
    from {{opacity:0; transform:translateY(40px);}}
    to {{opacity:1; transform:translateY(0);}}
}}

@keyframes fadeIn {{
    from {{opacity:0;}}
    to {{opacity:1;}}
}}

/* BUTTON ANIMATION */
button {{
    border-radius:14px !important;
    transition: all 0.25s ease !important;
}}

button:hover {{
    transform: scale(1.05);
}}

</style>
""", unsafe_allow_html=True)


#----------graphics-----

st.markdown("""
<div class="floating-bg"></div>

<style>
.floating-bg {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image: radial-gradient(circle at 20% 30%, rgba(255,255,255,0.15) 0px, transparent 200px),
                      radial-gradient(circle at 80% 70%, rgba(255,255,255,0.12) 0px, transparent 200px);
    z-index: -1;
}
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
# -------- AUDIO BLOCK --------
 # -------- SOFT BACKGROUND INSTRUMENTAL --------
st.markdown("""
<audio id="bgm" autoplay loop>
  <source src="https://cdn.pixabay.com/audio/2022/03/15/audio_3a9e4e2b75.mp3" type="audio/mp3">
</audio>

<script>
var audio = document.getElementById("bgm");
audio.volume = 0.25;
</script>
""", unsafe_allow_html=True)


# -------- MAIN PAGE --------
nickname = "Divya"

st.markdown(f'<div class="title">Welcome, {nickname}</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">This space grows slowly, like us.</div>', unsafe_allow_html=True)

st.divider()

# -------- SPOTIFY SONG SECTION --------
if "show_song" not in st.session_state:
    st.session_state.show_song = False

if st.button("🎧 Play Our Song"):
    st.session_state.show_song = True

if st.session_state.show_song:
    st.markdown("""
    <div style="
        margin-top:20px;
        animation: fadeIn 1s ease-in;
    ">
       <iframe data-testid="embed-iframe" style="border-radius:12px" src="https://open.spotify.com/embed/track/0FDlo7Rz1GQXjYz3y0UxPb?utm_source=generator&theme=0" width="100%" height="352" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>
    </div>
    """, unsafe_allow_html=True)

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

