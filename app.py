from flask import Flask, render_template, request, Response
import sqlite3
import csv
import io

app = Flask(__name__)

DATABASE = "survey.db"


# =========================
# データベース作成
# =========================

def init_db():

    conn = sqlite3.connect(DATABASE)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS responses (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            used TEXT,

            memory TEXT

        )
    """)

    conn.commit()

    conn.close()


# =========================
# アンケート画面
# =========================

@app.route("/")
def index():

    return render_template("index.html")


# =========================
# 回答保存
# =========================

@app.route("/submit", methods=["POST"])
def submit():

    used = request.form.get(
        "used",
        ""
    )

    memory = request.form.get(
        "memory",
        ""
    )


    conn = sqlite3.connect(DATABASE)


    conn.execute(
        """
        INSERT INTO responses
        (used, memory)

        VALUES (?, ?)
        """,

        (
            used,
            memory
        )
    )


    conn.commit()

    conn.close()


    return """
    <html lang="ja">

    <head>
        <meta charset="UTF-8">

        <title>
            回答ありがとうございました
        </title>
    </head>

    <body>

        <h1>
            🌸 ありがとうございました！
        </h1>

        <p>
            アンケートの回答を保存しました。
        </p>

        <p>
            <a href="/">
                もう一度回答する
            </a>
        </p>

        <p>
            <a href="/download_csv">
                CSVをダウンロードする
            </a>
        </p>

    </body>

    </html>
    """


# =========================
# CSVダウンロード
# =========================

@app.route("/download_csv")
def download_csv():

    conn = sqlite3.connect(DATABASE)

    cursor = conn.execute("""
        SELECT
            id,
            used,
            memory
        FROM responses
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    conn.close()


    output = io.StringIO()

    writer = csv.writer(output)


    # 見出し

    writer.writerow([
        "ID",
        "日焼け止め使用状況",
        "子どもの頃の思い出"
    ])


    # データ

    writer.writerows(rows)


    response = Response(
        output.getvalue(),
        mimetype="text/csv"
    )


    response.headers[
        "Content-Disposition"
    ] = (
        "attachment; "
        "filename=sunscreen_survey.csv"
    )


    return response


# =========================
# アプリ起動
# =========================

if __name__ == "__main__":

    init_db()

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )# 回答を保存
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
