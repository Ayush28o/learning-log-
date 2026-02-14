from flask import Flask, render_template, request, redirect
from supabase import create_client
from datetime import datetime
import os

app = Flask(__name__)

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

PASSWORD = os.environ.get("APP_PASSWORD")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if request.form.get("password") == PASSWORD:
            entries = supabase.table("entries").select("*").order("id", desc=True).execute().data
            return render_template("index.html", entries=entries)
        else:
            return render_template("login.html", error="Wrong password")
    return render_template("login.html")

@app.route("/add", methods=["POST"])
def add():
    supabase.table("entries").insert({
        "date": datetime.now().strftime("%d %B %Y"),
        "understood": request.form.get("understood"),
        "learned": request.form.get("learned"),
        "better": request.form.get("better")
    }).execute()
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

