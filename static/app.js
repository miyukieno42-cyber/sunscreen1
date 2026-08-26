const questions = document.querySelectorAll(".question");

let currentQuestion = 0;

const totalQuestions = questions.length;


// ==============================
// 進捗表示
// ==============================

function updateProgress() {
    const current = currentQuestion + 1;

    document.getElementById("currentQuestion").textContent = current;
    document.getElementById("totalQuestions").textContent = totalQuestions;

    const progress = (current / totalQuestions) * 100;

    document.getElementById("progress").style.width = progress + "%";
}


// ==============================
// 質問を表示
// ==============================

function showQuestion(number) {

    questions.forEach((question, index) => {

        question.classList.remove("active");

        if (index === number) {
            question.classList.add("active");
        }

    });

    updateProgress();

    // 画面を上に戻す
    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });
}


// ==============================
// 「次へ」ボタン
// ==============================

const nextButtons = document.querySelectorAll(".next-button");

nextButtons.forEach((button) => {

    button.addEventListener("click", () => {

        const current = questions[currentQuestion];

        // 必須項目をチェック
        const requiredInputs = current.querySelectorAll("input[required]");

        for (const input of requiredInputs) {

            if (!input.checkValidity()) {

                input.reportValidity();

                return;
            }
        }

        // 次の質問へ
        if (currentQuestion < totalQuestions - 1) {

            currentQuestion++;

            showQuestion(currentQuestion);
        }

    });

});


// ==============================
// 戻るボタンを作成
// ==============================

questions.forEach((question, index) => {

    // Q1には戻るボタンを作らない
    if (index === 0) {
        return;
    }

    // 送信ボタンがある最後のページにも
    // 戻るボタンを追加する
    const backButton = document.createElement("button");

    backButton.type = "button";
    backButton.className = "back-button";
    backButton.textContent = "← 戻る";

    // 戻るボタンを質問の一番下に追加
    question.appendChild(backButton);


    // 戻る処理
    backButton.addEventListener("click", () => {

        if (currentQuestion > 0) {

            currentQuestion--;

            showQuestion(currentQuestion);
        }

    });

});


// ==============================
// フォーム送信
// ==============================

const form = document.getElementById("surveyForm");

form.addEventListener("submit", (event) => {

    if (!form.checkValidity()) {

        event.preventDefault();

        form.reportValidity();

        return;
    }

});


// ==============================
// 「その他」の入力欄
// ==============================

const otherPairs = [
    ["feelingnowOther", "feelingnowOtherText"],
    ["importantOther", "importantOtherText"],
    ["wantOther", "wantOtherText"]
];


otherPairs.forEach(([optionId, textId]) => {

    const otherOption = document.getElementById(optionId);
    const otherText = document.getElementById(textId);


    if (otherOption && otherText) {

        otherOption.addEventListener("change", function () {

            if (this.checked) {

                otherText.style.display = "block";

            } else {

                otherText.style.display = "none";

                otherText.value = "";
            }

        });

    }

});


// ==============================
// 最初の質問を表示
// ==============================

showQuestion(0);
