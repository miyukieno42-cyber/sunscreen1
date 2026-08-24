from flask import Flask, render_template, request, redirect, url_for, Response
import sqlite3
import csv
import io
import os
from datetime import datetime

app = Flask(
    __name__,
    template_folder="../templates",
    static_folder="../static"
)

# Vercelの一時領域にDBを作成
DATABASE = "/tmp/survey.db"

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT,
            age_range TEXT,
            frequency TEXT,
            sunscreen_type TEXT,
            reason TEXT,
            feeling TEXT,
            product TEXT,
            usage_feeling TEXT,
            memory TEXT
        )
    """)
    conn.commit()
    return conn

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    # 子どもの頃
    age_range = request.form.get("age_range", "")
    gender = request.form.get("gender", "")
    frequency = request.form.get("frequency", "")
    feeling = request.form.get("feeling", "")

    sunscreen_type = request.form.getlist("sunscreen_type")
    reason = request.form.getlist("reason")

    product = request.form.get("product", "")
    usage_feeling = request.form.get("usage_feeling", "")
    memory = request.form.get("memory", "")

    # 現在
    feelingnow = request.form.get("feelingnow", "")
    frequencynow = request.form.get("frequencynow", "")
    valuenow = request.form.get("valuenow", "")
    value11now = request.form.get("value11now", "")
    important = request.form.get("important", "")
    want = request.form.get("want", "")

    # 「その他」の自由記述
    feelingnow_other = request.form.get("feelingnow_other", "")
    important_other = request.form.get("important_other", "")
    want_other = request.form.get("want_other", "")

    # その他の内容を回答に追加
    if feelingnow == "その他" and feelingnow_other:
        feelingnow = f"その他: {feelingnow_other}"

    if important == "その他" and important_other:
        important = f"その他: {important_other}"

    if want == "その他" and want_other:
        want = f"その他: {want_other}"

    sunscreen_type_text = ", ".join(sunscreen_type)
    reason_text = ", ".join(reason)

    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    sunscreen_type_text = ", ".join(sunscreen_type)
    reason_text = ", ".join(reason)

    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = get_db()
    conn.execute(
        """
        INSERT INTO responses
        (
            created_at,
            age_range,
            frequency,
            sunscreen_type,
            reason,
            feeling,
            product,
            usage_feeling,
            memory
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            created_at,
            age_range,
            frequency,
            sunscreen_type_text,
            reason_text,
            feeling,
            product,
            usage_feeling,
            memory
        )
    )
    conn.commit()
    conn.close()

    return redirect(url_for("thanks"))

@app.route("/thanks")
def thanks():
    return render_template("thanks.html")

@app.route("/download_csv")
def download_csv():
    if not os.path.exists(DATABASE):
        return "まだ回答データがありません。", 200

    conn = get_db()
    cursor = conn.execute(
        """
        SELECT
            id,
            created_at,
            age_range,
            frequency,
            sunscreen_type,
            reason,
            feeling,
            product,
            usage_feeling,
            memory
        FROM responses
        ORDER BY id
        """
    )
    rows = cursor.fetchall()
    conn.close()

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow([
        "ID",
        "回答日時",
        "年代",
        "使用頻度",
        "日焼け止めタイプ",
        "使用理由",
        "印象",
        "商品名",
        "使用時の気持ち",
        "思い出"
    ])
    writer.writerows(rows)

    response = Response(
        output.getvalue(),
        mimetype="text/csv; charset=utf-8"
    )
    response.headers["Content-Disposition"] = "attachment; filename=sunscreen_survey.csv"
    return response

if __name__ == "__main__":
    app.run(debug=True)
