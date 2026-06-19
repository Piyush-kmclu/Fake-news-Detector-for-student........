from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# Create Database and Table
def init_db():
    conn = sqlite3.connect("fake_news.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS news_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        news_text TEXT,
        prediction TEXT
    )
    """)

    conn.commit()
    conn.close()

# Analyze News
def predict_news(news):
    fake_keywords = ["shocking", "viral", "secret", "click here", "fake"]

    for word in fake_keywords:
        if word.lower() in news.lower():
            return "FAKE NEWS"

    return "REAL NEWS"

@app.route("/", methods=["GET", "POST"])
def home():
    result = ""
    history = []

    if request.method == "POST":
        news_text = request.form["news"]

        result = predict_news(news_text)

        conn = sqlite3.connect("fake_news.db")
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO news_history (news_text, prediction) VALUES (?, ?)",
            (news_text, result)
        )

        conn.commit()
        conn.close()

    conn = sqlite3.connect("fake_news.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, news_text, prediction FROM news_history ORDER BY id DESC"
    )
    history = cursor.fetchall()

    conn.close()

    return render_template(
        "index.html",
        result=result,
        history=history
    )

if __name__ == "__main__":
    init_db()
    app.run(debug=True)