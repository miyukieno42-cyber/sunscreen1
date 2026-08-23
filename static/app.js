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
