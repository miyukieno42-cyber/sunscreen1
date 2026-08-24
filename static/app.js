const questions = document.querySelectorAll(".question");
let currentQuestion = 0;
const totalQuestions = questions.length;

function updateProgress() {
    const current = currentQuestion + 1;
    document.getElementById("currentQuestion").textContent = current;
    document.getElementById("totalQuestions").textContent = totalQuestions;
    const progress = (current / totalQuestions) * 100;
    document.getElementById("progress").style.width = progress + "%";
}

function showQuestion(number) {
    questions.forEach((question, index) => {
        question.classList.remove("active");
        if (index === number) {
            question.classList.add("active");
        }
    });
    updateProgress();
}

const nextButtons = document.querySelectorAll(".next-button");
nextButtons.forEach((button) => {
    button.addEventListener("click", () => {
        const current = questions[currentQuestion];
        const requiredInputs = current.querySelectorAll("input[required]");

        for (const input of requiredInputs) {
            if (!input.checkValidity()) {
                input.reportValidity();
                return;
            }
        }

        if (currentQuestion < totalQuestions - 1) {
            currentQuestion++;
            showQuestion(currentQuestion);
        }
    });
});

const form = document.getElementById("surveyForm");
form.addEventListener("submit", (event) => {
    if (!form.checkValidity()) {
        event.preventDefault();
        form.reportValidity();
        return;
    }
});

showQuestion(0);

// 「その他」を選んだときだけ記述欄を表示する
const otherPairs = [
    ["feelingnowOther", "feelingnowOtherText"],
    ["importantOther", "importantOtherText"],
    ["wantOther", "wantOtherText"]
];

otherPairs.forEach(([checkboxId, textId]) => {
    const otherOption = document.getElementById(checkboxId);
    const otherText = document.getElementById(textId);

    if (otherOption && otherText) {
        otherOption.addEventListener("change", () => {
            if (otherOption.checked) {
                otherText.style.display = "block";
            } else {
                otherText.style.display = "none";
                otherText.value = "";
            }
        });
    }
});
const feelingnowOther = document.getElementById("feelingnowOther");
const feelingnowOtherText = document.getElementById("feelingnowOtherText");

if (feelingnowOther && feelingnowOtherText) {
    feelingnowOther.addEventListener("change", function () {
        if (this.checked) {
            feelingnowOtherText.style.display = "block";
        } else {
            feelingnowOtherText.style.display = "none";
            feelingnowOtherText.value = "";
        }
    });
}
