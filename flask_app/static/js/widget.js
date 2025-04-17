// Перетаскивание функциональности
let isDragging = false;
const widget = document.getElementById('avatarWidget');

widget.addEventListener('mousedown', (e) => {
    isDragging = true;
    let offsetX = e.clientX - widget.getBoundingClientRect().left;
    let offsetY = e.clientY - widget.getBoundingClientRect().top;

    const mouseMoveHandler = (e) => {
        if (isDragging) {
            let newLeft = e.clientX - offsetX;
            let newTop = e.clientY - offsetY;

            // Ограничиваем перемещение виджета в пределах окна
            newLeft = Math.max(0, Math.min(window.innerWidth - widget.clientWidth, newLeft));
            newTop = Math.max(0, Math.min(window.innerHeight - widget.clientHeight, newTop));

            widget.style.left = newLeft + 'px';
            widget.style.top = newTop + 'px';
        }
    };

    const mouseUpHandler = () => {
        isDragging = false;
        document.removeEventListener('mousemove', mouseMoveHandler);
        document.removeEventListener('mouseup', mouseUpHandler);
    };

    document.addEventListener('mousemove', mouseMoveHandler);
    document.addEventListener('mouseup', mouseUpHandler);
});

// Поддержка для сенсорных устройств
widget.addEventListener('touchstart', (e) => {
    isDragging = true;
    let offsetX = e.touches[0].clientX - widget.getBoundingClientRect().left;
    let offsetY = e.touches[0].clientY - widget.getBoundingClientRect().top;

    const touchMoveHandler = (e) => {
        if (isDragging) {
            let newLeft = e.touches[0].clientX - offsetX;
            let newTop = e.touches[0].clientY - offsetY;

            // Ограничиваем перемещение виджета в пределах окна
            newLeft = Math.max(0, Math.min(window.innerWidth - widget.clientWidth, newLeft));
            newTop = Math.max(0, Math.min(window.innerHeight - widget.clientHeight, newTop));

            widget.style.left = newLeft + 'px';
            widget.style.top = newTop + 'px';
        }
    };

    const touchEndHandler = () => {
        isDragging = false;
        document.removeEventListener('touchmove', touchMoveHandler);
        document.removeEventListener('touchend', touchEndHandler);
    };

    document.addEventListener('touchmove', touchMoveHandler);
    document.addEventListener('touchend', touchEndHandler);
});

// Функция для смены аватара
function changeAvatar(newSrc) {
    const imgElement = document.getElementById('avatarImg');
    imgElement.src = newSrc;
}