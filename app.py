from flask import Flask, render_template, request, redirect, url_for, Response
import sqlite3
import csv
import io
from datetime import datetime


# ========================================
# Flaskアプリを作る
# ========================================

app = Flask(__name__)


# ========================================
# データベースの名前
# ========================================

DATABASE = "/tmp/survey.db"


# ========================================
# データベースを作る関数
# ========================================

def init_db():

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

    conn.close()


# ========================================
# トップページ
# ========================================

@app.route("/")
def index():

    return render_template("index.html")


# ========================================
# アンケート回答を受け取る
# ========================================

@app.route("/submit", methods=["POST"])
def submit():

    # ----------------------------
    # 単一選択
    # ----------------------------

    age_range = request.form.get(
        "age_range",
        ""
    )

    frequency = request.form.get(
        "frequency",
        ""
    )

    feeling = request.form.get(
        "feeling",
        ""
    )


    # ----------------------------
    # 複数選択
    # ----------------------------

    sunscreen_type = request.form.getlist(
        "sunscreen_type"
    )

    reason = request.form.getlist(
        "reason"
    )


    # ----------------------------
    # 記述
    # ----------------------------

    product = request.form.get(
        "product",
        ""
    )

    usage_feeling = request.form.get(
        "usage_feeling",
        ""
    )

    memory = request.form.get(
        "memory",
        ""
    )


    # ----------------------------
    # 複数選択を文字列に変換
    # ----------------------------

    sunscreen_type_text = ", ".join(
        sunscreen_type
    )

    reason_text = ", ".join(
        reason
    )


    # ----------------------------
    # 回答日時
    # ----------------------------

    created_at = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )


    # ----------------------------
    # データベースに保存
    # ----------------------------

    conn = sqlite3.connect(DATABASE)

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


    # ----------------------------
    # 完了画面へ
    # ----------------------------

    return redirect(
        url_for("thanks")
    )


# ========================================
# 送信完了ページ
# ========================================

@app.route("/thanks")
def thanks():

    return render_template(
        "thanks.html"
    )


# ========================================
# CSVダウンロード
# ========================================

@app.route("/download_csv")
def download_csv():

    conn = sqlite3.connect(DATABASE)

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


    # ----------------------------
    # CSVをメモリ上で作る
    # ----------------------------

    output = io.StringIO()

    writer = csv.writer(
        output
    )


    # ヘッダー

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


    # データ

    writer.writerows(
        rows
    )


    # ----------------------------
    # CSVを返す
    # ----------------------------

    response = Response(
        output.getvalue(),
        mimetype="text/csv; charset=utf-8"
    )


    response.headers[
        "Content-Disposition"
    ] = (
        "attachment; "
        "filename=sunscreen_survey.csv"
    )


    return response


# ========================================
# アプリ起動
# ========================================

if __name__ == "__main__":

    init_db()

    app.run(
        debug=True
    )
