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

    # 最初にテーブルを作成
    conn.execute("""
        CREATE TABLE IF NOT EXISTS responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT,

            age_range TEXT,
            gender TEXT,
            frequency TEXT,
            sunscreen_type TEXT,
            reason TEXT,
            feeling TEXT,
            product TEXT,
            usage_feeling TEXT,
            memory TEXT,

            feelingnow TEXT,
            frequencynow TEXT,
            valuenow TEXT,
            value11now TEXT,
            important TEXT,
            want TEXT,

            feelingnow_other TEXT,
            important_other TEXT,
            want_other TEXT
        )
    """)

    conn.commit()

    # すでに古いDBが存在する場合に備えて、
    # 足りないカラムを自動的に追加する
    existing_columns = {
        row[1]
        for row in conn.execute("PRAGMA table_info(responses)").fetchall()
    }

    required_columns = {
        "gender": "TEXT",
        "feelingnow": "TEXT",
        "frequencynow": "TEXT",
        "valuenow": "TEXT",
        "value11now": "TEXT",
        "important": "TEXT",
        "want": "TEXT",
        "feelingnow_other": "TEXT",
        "important_other": "TEXT",
        "want_other": "TEXT"
    }

    for column, column_type in required_columns.items():
        if column not in existing_columns:
            conn.execute(
                f"ALTER TABLE responses ADD COLUMN {column} {column_type}"
            )

    conn.commit()

    return conn


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():

    # ==========================================
    # 子どものころ
    # ==========================================

    age_range = request.form.get("age_range", "")
    gender = request.form.get("gender", "")
    frequency = request.form.get("frequency", "")
    feeling = request.form.get("feeling", "")

    # 複数選択
    sunscreen_type = request.form.getlist("sunscreen_type")
    reason = request.form.getlist("reason")

    product = request.form.get("product", "")
    usage_feeling = request.form.get("usage_feeling", "")
    memory = request.form.get("memory", "")

    # ==========================================
    # 現在
    # ==========================================

    feelingnow = request.form.get("feelingnow", "")
    frequencynow = request.form.get("frequencynow", "")
    valuenow = request.form.get("valuenow", "")
    value11now = request.form.get("value11now", "")
    important = request.form.get("important", "")
    want = request.form.get("want", "")

    # ==========================================
    # 「その他」の自由記述
    # ==========================================

    feelingnow_other = request.form.get("feelingnow_other", "")
    important_other = request.form.get("important_other", "")
    want_other = request.form.get("want_other", "")

    # その他を選択していた場合、
    # 「その他: ○○」という形で保存
    if feelingnow == "その他" and feelingnow_other:
        feelingnow = f"その他: {feelingnow_other}"

    if important == "その他" and important_other:
        important = f"その他: {important_other}"

    if want == "その他" and want_other:
        want = f"その他: {want_other}"

    # ==========================================
    # 複数選択を文字列に変換
    # ==========================================

    sunscreen_type_text = ", ".join(sunscreen_type)
    reason_text = ", ".join(reason)

    # ==========================================
    # 回答日時
    # ==========================================

    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # ==========================================
    # データベースへ保存
    # ==========================================

    conn = get_db()

    conn.execute(
        """
        INSERT INTO responses
        (
            created_at,

            age_range,
            gender,
            frequency,
            sunscreen_type,
            reason,
            feeling,
            product,
            usage_feeling,
            memory,

            feelingnow,
            frequencynow,
            valuenow,
            value11now,
            important,
            want,

            feelingnow_other,
            important_other,
            want_other
        )
        VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
            ?, ?, ?, ?, ?, ?,
            ?, ?, ?
        )
        """,
        (
            created_at,

            age_range,
            gender,
            frequency,
            sunscreen_type_text,
            reason_text,
            feeling,
            product,
            usage_feeling,
            memory,

            feelingnow,
            frequencynow,
            valuenow,
            value11now,
            important,
            want,

            feelingnow_other,
            important_other,
            want_other
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
            gender,
            frequency,
            sunscreen_type,
            reason,
            feeling,
            product,
            usage_feeling,
            memory,

            feelingnow,
            frequencynow,
            valuenow,
            value11now,
            important,
            want
        FROM responses
        ORDER BY id
        """
    )

    rows = cursor.fetchall()

    conn.close()

    # ==========================================
    # CSV作成
    # ==========================================

    output = io.StringIO()

    writer = csv.writer(output)

    writer.writerow([
        "ID",
        "回答日時",

        "年代",
        "性別",
        "子どもの頃の使用頻度",
        "子どもの頃の日焼け止めタイプ",
        "子どもの頃の使用理由",
        "子どもの頃の日焼け止めの印象",
        "商品名",
        "使用時の気持ち",
        "思い出",

        "現在の日焼け止めのマイナスイメージ",
        "現在の日焼け止めの使用頻度",
        "現在の日焼け止めの印象",
        "現在の日焼け止めの重要度",
        "現在の日焼け止めを買うときに重視すること",
        "おもしろい日焼け止めで重視すること"
    ])

    writer.writerows(rows)

    # ==========================================
    # CSVをダウンロード
    # ==========================================

    response = Response(
        output.getvalue(),
        mimetype="text/csv; charset=utf-8"
    )

    response.headers[
        "Content-Disposition"
    ] = "attachment; filename=sunscreen_survey.csv"

    return response


if __name__ == "__main__":
    app.run(debug=True)
