from flask import Flask, render_template, request, redirect, url_for, Response
import csv
import io
import os
from datetime import datetime
import psycopg


app = Flask(
    __name__,
    template_folder="../templates",
    static_folder="../static"
)


# =========================================================
# Neon PostgreSQL の接続先を取得
# =========================================================
def get_database_url():
    """
    Vercel + Neon で設定されている接続情報を
    上から順番に探します。
    """

    possible_urls = [
        os.environ.get("DATABASE_URL"),
        os.environ.get("POSTGRES_URL"),
        os.environ.get("POSTGRES_URL_NON_POOLING"),
        os.environ.get("DATABASE_URL_UNPOOLED"),
        os.environ.get("POSTGRES_PRISMA_URL"),
    ]

    for url in possible_urls:
        if url:
            return url

    raise RuntimeError(
        "データベース接続情報が見つかりません。"
        "VercelのEnvironment Variablesを確認してください。"
    )


# =========================================================
# データベース接続
# =========================================================
def get_db():
    database_url = get_database_url()

    conn = psycopg.connect(database_url)

    # テーブルがなければ自動で作成
    conn.execute("""
        CREATE TABLE IF NOT EXISTS responses (
            id SERIAL PRIMARY KEY,
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

    return conn


# =========================================================
# アンケートページ
# =========================================================
@app.route("/")
def index():
    return render_template("index.html")


# =========================================================
# アンケート回答を保存
# =========================================================
@app.route("/submit", methods=["POST"])
def submit():

    # =====================================================
    # 子どものころ
    # =====================================================

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

    # =====================================================
    # 「その他」の入力
    # =====================================================

    # Q5：使用した理由
    reason_other = request.form.get("reason_other", "").strip()

    if reason_other:
        reason.append(f"その他: {reason_other}")

    # =====================================================
    # 現在
    # =====================================================

    feelingnow = request.form.get("feelingnow", "")
    frequencynow = request.form.get("frequencynow", "")
    valuenow = request.form.get("valuenow", "")
    value11now = request.form.get("value11now", "")
    important = request.form.get("important", "")
    want = request.form.get("want", "")

    # =====================================================
    # 現在の「その他」
    # =====================================================

    feelingnow_other = request.form.get(
        "feelingnow_other",
        ""
    ).strip()

    important_other = request.form.get(
        "important_other",
        ""
    ).strip()

    want_other = request.form.get(
        "want_other",
        ""
    ).strip()

    # =====================================================
    # 「その他」を選択していた場合
    # =====================================================

    if feelingnow == "その他" and feelingnow_other:
        feelingnow = f"その他: {feelingnow_other}"

    if important == "その他" and important_other:
        important = f"その他: {important_other}"

    if want == "その他" and want_other:
        want = f"その他: {want_other}"

    # =====================================================
    # 複数選択を文字列に変換
    # =====================================================

    sunscreen_type_text = ", ".join(sunscreen_type)
    reason_text = ", ".join(reason)

    # =====================================================
    # 回答日時
    # =====================================================

    created_at = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    # =====================================================
    # Neon PostgreSQL に保存
    # =====================================================

    conn = get_db()

    try:

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
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s
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

    finally:
        conn.close()

    return redirect(url_for("thanks"))


# =========================================================
# 完了ページ
# =========================================================
@app.route("/thanks")
def thanks():
    return render_template("thanks.html")


# =========================================================
# CSVダウンロード
# =========================================================
@app.route("/download_csv")
def download_csv():

    conn = get_db()

    try:

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

    finally:
        conn.close()

    # =====================================================
    # 回答がない場合
    # =====================================================

    if not rows:
        return "まだ回答データがありません。", 200

    # =====================================================
    # CSV作成
    # =====================================================

    output = io.StringIO(newline="")

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

    # Excelでも日本語が文字化けしにくいUTF-8 BOM
    csv_data = output.getvalue().encode("utf-8-sig")

    response = Response(
        csv_data,
        mimetype="text/csv"
    )

    response.headers["Content-Disposition"] = (
        "attachment; filename=sunscreen_survey.csv"
    )

    return response


# =========================================================
# ローカルで実行した場合
# =========================================================

if __name__ == "__main__":
    app.run(debug=True)
