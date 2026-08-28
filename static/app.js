const questions = document.querySelectorAll(".question");

let currentQuestion = 0;

const totalQuestions = questions.length;


/* =========================
   進捗バー
========================= */

function updateProgress() {

    const current = currentQuestion + 1;

    document.getElementById("currentQuestion").textContent = current;
    document.getElementById("totalQuestions").textContent = totalQuestions;

    const progress = (current / totalQuestions) * 100;

    document.getElementById("progress").style.width = progress + "%";
}


/* =========================
   質問を表示
========================= */

function showQuestion(number) {

    questions.forEach((question, index) => {

        question.classList.remove("active");

        if (index === number) {
            question.classList.add("active");
        }

    });

    updateProgress();
}


/* =========================
   次へボタン
========================= */

const nextButtons = document.querySelectorAll(".next-button");

nextButtons.forEach((button) => {

    button.addEventListener("click", () => {

        const current = questions[currentQuestion];

        // 必須項目をチェック
        const requiredInputs =
            current.querySelectorAll("input[required]");

        for (const input of requiredInputs) {

            if (!input.checkValidity()) {

                input.reportValidity();

                return;
            }
        }


        // 次のページへ
        if (currentQuestion < totalQuestions - 1) {

            currentQuestion++;

            showQuestion(currentQuestion);

            window.scrollTo({
                top: 0,
                behavior: "smooth"
            });
        }

    });

});


/* =========================
   戻るボタン
========================= */

/*
   HTMLにすでに戻るボタンがあるので、
   JavaScriptでは新しく作らない。
*/

const backButtons =
    document.querySelectorAll(".back-button");

backButtons.forEach((button) => {

    button.addEventListener("click", () => {

        if (currentQuestion > 0) {

            currentQuestion--;

            showQuestion(currentQuestion);

            window.scrollTo({
                top: 0,
                behavior: "smooth"
            });

        }

    });

});


/* =========================
   送信時のチェック
========================= */

const form =
    document.getElementById("surveyForm");

form.addEventListener("submit", (event) => {

    if (!form.checkValidity()) {

        event.preventDefault();

        form.reportValidity();

        return;
    }

});


/* =========================
   最初の質問
========================= */

showQuestion(0);


/* =========================
   「その他」の入力欄
========================= */


/* -------------------------
   Q10
------------------------- */

const feelingnowOther =
    document.getElementById("feelingnowOther");

const feelingnowOtherText =
    document.getElementById("feelingnowOtherText");

if (feelingnowOther && feelingnowOtherText) {

    feelingnowOther.addEventListener("change", function () {

        if (this.checked) {

            feelingnowOtherText.style.display = "block";

            feelingnowOtherText.focus();

        } else {

            feelingnowOtherText.style.display = "none";

            feelingnowOtherText.value = "";

        }

    });

}


/* -------------------------
   Q14
------------------------- */

const importantOther =
    document.getElementById("importantOther");

const importantOtherText =
    document.getElementById("importantOtherText");

if (importantOther && importantOtherText) {

    importantOther.addEventListener("change", function () {

        if (this.checked) {

            importantOtherText.style.display = "block";

            importantOtherText.focus();

        } else {

            importantOtherText.style.display = "none";

            importantOtherText.value = "";

        }

    });

}


/* -------------------------
   Q15
------------------------- */

const wantOther =
    document.getElementById("wantOther");

const wantOtherText =
    document.getElementById("wantOtherText");

if (wantOther && wantOtherText) {

    wantOther.addEventListener("change", function () {

        if (this.checked) {

            wantOtherText.style.display = "block";

            wantOtherText.focus();

        } else {

            wantOtherText.style.display = "none";

            wantOtherText.value = "";

        }

    });

}

/* -------------------------
   Q5
------------------------- */

const reasonOther =
    document.getElementById("reasonOther");

const reasonOtherText =
    document.getElementById("reasonOtherText");

if (reasonOther && reasonOtherText) {

    reasonOther.addEventListener("change", function () {

        if (this.checked) {

            reasonOtherText.style.display = "block";

            reasonOtherText.focus();

        } else {

            reasonOtherText.style.display = "none";

            reasonOtherText.value = "";

        }

    });

}
