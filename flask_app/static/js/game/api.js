const API_BASE_URL = "http://127.0.0.1:5000/";

// Получаем CSRF-токен из мета-тега
const csrfToken = document.querySelector('meta[name="csrf-token"]').content;

// Получить информацию о предмете
export async function getItem(itemId) {
    const response = await fetch(`${API_BASE_URL}/items/${itemId}`, {
        headers: {
            "X-CSRF-TOKEN": csrfToken,
        },
    });
    if (!response.ok) throw new Error("Ошибка при получении предмета");
    return response.json();
}

// Провести молитву
export async function performPrayer(userId, prayerId) {
    const response = await fetch(`${API_BASE_URL}/prayer`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRF-TOKEN": csrfToken,
        },
        body: JSON.stringify({ user_id: userId, prayer_id: prayerId }),
    });
    if (!response.ok) throw new Error("Ошибка при проведении молитвы");
    return response.json();
}

// Получить валюту пользователя
export async function getCurrency(userId) {
    const response = await fetch(`${API_BASE_URL}/currency/${userId}`, {
        headers: {
            "X-CSRF-TOKEN": csrfToken,
        },
    });
    if (!response.ok) throw new Error("Ошибка при получении валюты");
    return response.json();
}