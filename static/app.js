// ============================
// アンケートの質問を取得
// ============================

const questions =
    document.querySelectorAll(".question");


// 現在の質問番号

let currentQuestion = 0;


// 全質問数

const totalQuestions =
    questions.length;


// HTMLの表示を更新

function updateProgress() {

    const current =
        currentQuestion + 1;


    document.getElementById(
        "currentQuestion"
    ).textContent = current;


    document.getElementById(
        "totalQuestions"
    ).textContent = totalQuestions;


    const progress =
        (current / totalQuestions) * 100;


    document.getElementById(
        "progress"
    ).style.width = progress + "%";
}


// ============================
// 質問を表示する
// ============================

function showQuestion(number) {

    questions.forEach(
        (question, index) => {

            question.classList.remove(
                "active"
            );


            if (index === number) {

                question.classList.add(
                    "active"
                );

            }

        }
    );


    updateProgress();
}


// ============================
// 「次へ」ボタン
// ============================

const nextButtons =
    document.querySelectorAll(
        ".next-button"
    );


nextButtons.forEach(
    (button) => {

        button.addEventListener(
            "click",
            () => {

                const current =
                    questions[currentQuestion];


                // ----------------------------
                // 必須回答のチェック
                // ----------------------------

                const requiredInputs =
                    current.querySelectorAll(
                        "input[required]"
                    );


                for (
                    const input
                    of requiredInputs
                ) {

                    if (
                        !input.checkValidity()
                    ) {

                        input.reportValidity();

                        return;

                    }

                }


                // ----------------------------
                // 次の質問へ
                // ----------------------------

                if (
                    currentQuestion
                    <
                    totalQuestions - 1
                ) {

                    currentQuestion++;

                    showQuestion(
                        currentQuestion
                    );

                }

            }
        );

    }
);


// ============================
// 送信
// ============================

const form =
    document.getElementById(
        "surveyForm"
    );


form.addEventListener(
    "submit",
    (event) => {

        // 最後の質問でも
        // 必須項目を確認

        if (!form.checkValidity()) {

            event.preventDefault();

            form.reportValidity();

            return;

        }

    }
);


// ============================
// 最初の質問を表示
// ============================

showQuestion(0);
