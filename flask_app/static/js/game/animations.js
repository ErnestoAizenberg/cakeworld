// Анимация алтаря
export function animateAltar() {
    const altar = document.getElementById("altar");
    altar.animate(
        [
            { transform: "scale(1)", opacity: 1 },
            { transform: "scale(1.1)", opacity: 0.8 },
            { transform: "scale(1)", opacity: 1 },
        ],
        {
            duration: 1000,
            iterations: 1,
        }
    );
}

// Анимация появления кода
export function animateCodeReveal(codeElement) {
    codeElement.animate(
        [
            { opacity: 0, transform: "translateY(-20px)" },
            { opacity: 1, transform: "translateY(0)" },
        ],
        {
            duration: 500,
            fill: "forwards",
        }
    );
}

// Анимация неудачной молитвы
export function animatePrayerFailure() {
    const codex = document.getElementById("codex");
    codex.animate(
        [
            { transform: "rotate(0deg)", opacity: 1 },
            { transform: "rotate(10deg)", opacity: 0.8 },
            { transform: "rotate(-10deg)", opacity: 0.8 },
            { transform: "rotate(0deg)", opacity: 1 },
        ],
        {
            duration: 500,
            iterations: 2,
        }
    );
}