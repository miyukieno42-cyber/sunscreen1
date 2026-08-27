const questions = document.querySelectorAll(".question");
let currentQuestion = 0;

// CURRENTの説明ページは「質問数」に含めない
const actualQuestions = document.querySelectorAll(
    ".question:not(.section-intro-page)"
);

const totalQuestions = actualQuestions.length;

// ==============================
// 進捗表示
// ==============================
function updateProgress() {
    const currentPage = questions[currentQuestion];

    // CURRENTの説明ページなら、Q10の次として表示
    if (currentPage.classList.contains("section-intro-page")) {
        document.getElementById("currentQuestion").textContent =
            actualQuestions.length > 0
                ? Array.from(actualQuestions).indexOf(
                      questions[currentQuestion - 1]
                  ) + 1
                : 1;
    } else {
        const actualIndex = Array.from(actualQuestions).indexOf(currentPage);

        document.getElementById("currentQuestion").textContent =
            actualIndex + 1;
    }

    document.getElementById("totalQuestions").textContent = totalQuestions;

    // 現在のページに合わせて進捗バーを動かす
    let progressPercent;

    if (currentPage.classList.contains("section-intro-page")) {
        // CURRENT説明ページはQ10とQ11の間なので10問目の位置
        progressPercent = (10 / totalQuestions) * 100;
    } else {
        const actualIndex = Array.from(actualQuestions).indexOf(currentPage);
        progressPercent = ((actualIndex + 1) / totalQuestions) * 100;
    }

    document.getElementById("progress").style.width =
        progressPercent + "%";
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

    // Q1では「戻る」を表示しない
    const backButtons = questions[number].querySelectorAll(".back-button");

    backButtons.forEach((button) => {
        if (number === 0) {
            button.style.display = "none";
        } else {
            button.style.display = "block";
        }
    });

    // ページが変わったら上まで戻す
    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });
}


// ==============================
// 次へボタン
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

        // 次のページへ
        if (currentQuestion < questions.length - 1) {
            currentQuestion++;
            showQuestion(currentQuestion);
        }
    });
});


// ==============================
// 戻るボタン
// ==============================
const backButtons = document.querySelectorAll(".back-button");

backButtons.forEach((button) => {
    button.addEventListener("click", () => {

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

otherPairs.forEach(([otherId, textId]) => {
    const otherOption = document.getElementById(otherId);
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
// 最初のページを表示
// ==============================
showQuestion(0);
