
    document.addEventListener("DOMContentLoaded", function() {
        const breadcrumbList = document.getElementById('breadcrumb-list');
        const path = window.location.pathname.split('/').filter(Boolean);
        
        // Добавляем каждый сегмент URL в навигацию
        let fullPath = '';
        path.forEach((segment, index) => {
            fullPath += '/' + segment;
            const listItem = document.createElement('li');

            // Если это последний сегмент, делаем его не кликабельным
            if (index === path.length - 1) {
                listItem.innerHTML = `<span>${decodeURIComponent(segment.replace(/-/g, ' '))}</span>`;
            } else {
                listItem.innerHTML = `<a href="${fullPath}">${decodeURIComponent(segment.replace(/-/g, ' '))}</a>`;
            }

            breadcrumbList.appendChild(listItem);
            
            // Анимация для появления элементов по горизонтали
            anime({
                targets: listItem,
                opacity: [0, 1],
                translateX: [-20, 0], // Анимация сдвига влево по оси X
                easing: 'easeOutExpo',
                duration: 500,
                delay: index * 200 // задержка для каждого следующего элемента
            });
        });
    });