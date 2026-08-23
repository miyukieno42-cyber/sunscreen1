from flask import Flask, render_template, request

import sqlite3

app = Flask(__name__)


# データベースを作る
def init_db():

    conn = sqlite3.connect("survey.db")

    conn.execute("""
        CREATE TABLE IF NOT EXISTS responses (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            used TEXT,

            memory TEXT

        )
    """)

    conn.commit()

    conn.close()


# アンケート画面
@app.route("/")
def index():

    return render_template("index.html")


# 回答を保存
@app.route("/submit", methods=["POST"])
def submit():

    used = request.form.get("used", "")

    memory = request.form.get("memory", "")


    conn = sqlite3.connect("survey.db")


    conn.execute(
        """
        INSERT INTO responses
        (used, memory)

        VALUES (?, ?)
        """,

        (used, memory)
    )


    conn.commit()

    conn.close()


    return """
    <h1>🌸 ありがとうございました！</h1>

    <p>
        アンケートの回答を保存しました。
    </p>

    <a href="/">
        もう一度回答する
    </a>
    """


if __name__ == "__main__":

    init_db()

    app.run(
        host="0.0.0.0",
        port=5000
    )
