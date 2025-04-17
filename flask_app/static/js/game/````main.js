import { performPrayer, getCurrency } from "./api.js";
import { animateAltar, animateCodeReveal, animatePrayerFailure } from "./animations.js";

const userId = 1; // ID пользователя (можно динамически задавать)
const prayerId = 1; // ID молитвы (можно динамически задавать)

const performPrayerButton = document.getElementById("perform-prayer");
const resultDiv = document.getElementById("result");

// Элементы для отображения валюты
const coinsDisplay = document.getElementById("coins");
const stonesDisplay = document.getElementById("stones");
const gemsDisplay = document.getElementById("gems");

// Функция для обновления валюты
async function updateCurrencyDisplay() {
    try {
        const currency = await getCurrency(userId);
        coinsDisplay.textContent = currency.coins;
        stonesDisplay.textContent = currency.stones;
        gemsDisplay.textContent = currency.gems;
    } catch (error) {
        console.error("Ошибка при обновлении валюты:", error);
    }
}

// Обновляем валюту при загрузке страницы
updateCurrencyDisplay();

performPrayerButton.addEventListener("click", async () => {
    try {
        // Анимация алтаря
        animateAltar();

        // Выполнение молитвы через API
        const prayerResult = await performPrayer(userId, prayerId);

        // Отображение результата
        if (prayerResult.item_code) {
            resultDiv.innerHTML = `
                <p>Вы получили код: <strong>${prayerResult.item_code.code}</strong></p>
                <p>Предмет: ${prayerResult.item_code.item_name}</p>
            `;
            animateCodeReveal(resultDiv);
        } else {
            resultDiv.innerHTML = "<p>К сожалению, вы ничего не получили.</p>";
            animatePrayerFailure();
        }

        // Обновляем валюту после молитвы
        await updateCurrencyDisplay();
    } catch (error) {
        resultDiv.innerHTML = `<p>Ошибка: ${error.message}</p>`;
    }
});