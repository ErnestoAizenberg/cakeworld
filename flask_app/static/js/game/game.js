document.addEventListener('DOMContentLoaded', () => {
    const csrfToken = document.querySelector('.container').dataset.csrfToken;

    const state = {
        activeMenu: 'shop',
        resources: { coins: 0, stones: 0, gems: 0 },
        quests: { daily: [], weekly: [] },
        inventory: [],
        achievements: []
    };

    function changeMenu(menuId) {
        state.activeMenu = menuId;
        render();
    }

    async function fetchData() {
        try {
            const response = await fetch('/data', { headers: { 'X-CSRF-TOKEN': csrfToken } });
            if (!response.ok) throw new Error('Ошибка загрузки данных');
            const data = await response.json();
            updateState(data);
            render();
        } catch (error) {
            console.error(error);
        }
    }

    function updateState(data) {
        state.resources = data.resources;
        state.quests.daily = data.dailyQuests;
        state.quests.weekly = data.weeklyQuests;
        state.inventory = data.inventory;
        state.achievements = data.achievements;
    }

    function render() {
        updateResources();
        updateContent();
        displayActiveMenu();
    }

    function updateResources() {
        const resourceElements = document.querySelectorAll('.resource-item');
        resourceElements.forEach(el => {
            const resourceType = el.dataset.resourceType;
            el.querySelector('.resource-value').textContent = state.resources[resourceType];
        });
    }

    function updateContent() {
        document.getElementById('daily-quests').innerHTML = renderQuests(state.quests.daily);
        document.getElementById('weekly-quests').innerHTML = renderQuests(state.quests.weekly);
        document.getElementById('inventory-grid').innerHTML = renderInventory(state.inventory);
        document.getElementById('achievement-grid').innerHTML = renderAchievements(state.achievements);
    }

    function renderQuests(quests) {
        return quests.map(quest => `
            <div class="quest-card">
                <div class="quest-title">${quest.title}</div>
                <div class="quest-progress">
                    <div class="progress-bar" style="width: ${(quest.progress / quest.goal) * 100}%"></div>
                </div>
                <div class="quest-reward">
                    <i class="fas fa-${quest.reward.type === 'coins' ? 'coins' : quest.reward.type === 'stones' ? 'star' : 'gem'}"></i>
                    <span>${quest.reward.amount}</span>
                </div>
            </div>
        `).join('');
    }

    function renderInventory(inventory) {
        return inventory.map(item => `
            <div class="item-card">
                <img src="${item.image}" class="item-image" alt="${item.name}">
                <div>${item.name}</div>
                <div>Количество: ${item.quantity}</div>
            </div>
        `).join('');
    }

    function renderAchievements(achievements) {
        return achievements.map(achievement => `
            <div class="achievement-card">
                <div class="achievement-title">${achievement.title}</div>
                <div class="achievement-description">${achievement.description}</div>
                <div class="achievement-progress">
                    <div class="achievement-progress-bar" style="width: ${(achievement.progress / achievement.goal) * 100}%"></div>
                </div>
            </div>
        `).join('');
    }

    function displayActiveMenu() {
        document.querySelectorAll('#content > div').forEach(div => {
            div.style.display = 'none';
        });
        const activeContent = document.getElementById(state.activeMenu);
        if (activeContent) {
            activeContent.style.display = 'block';
        }
    }

    // Функции для молитвы
    function createStars() {
        const overlay = document.getElementById('prayerOverlay');
        overlay.style.display = 'flex'; // Показываем оверлей
        for (let i = 0; i < 100; i++) {
            const star = document.createElement('div');
            star.className = 'star';
            star.style.left = `${Math.random() * 100}%`;
            star.style.top = `${Math.random() * 100}%`;
            star.style.animationDelay = `${Math.random() * 2}s`;
            overlay.appendChild(star);
        }
    }

    function startPrayer() {
        const overlay = document.getElementById('prayerOverlay');
        overlay.style.display = 'flex';
        createStars();

        // Симуляция запроса на сервер
        setTimeout(() => {
            showResult();
        }, 3000);
    }


    function showResult() {
        const result = document.getElementById('prayerResult');
        result.classList.add('active');
    }

    function closeResult() {
        const overlay = document.getElementById('prayerOverlay');
        overlay.style.display = 'none';
        overlay.innerHTML = '<div class="prayer-result" id="prayerResult"></div>'; // Сброс содержания
    }

    // Обработаны события меню
    document.querySelectorAll('.mobile-menu-item').forEach(item => {
        item.addEventListener('click', () => changeMenu(item.dataset.menuId));
    });

    // Инициализация
    fetchData();
    changeMenu('shop'); // Открываем магазин по умолчанию
});