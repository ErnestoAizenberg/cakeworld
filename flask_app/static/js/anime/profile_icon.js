
  


  document.addEventListener("DOMContentLoaded", function() {
    // Анимация при загрузке страницы
    anime({
      targets: '.profile-icon',
      opacity: [0, 1],
      translateY: [-10, 0],
      duration: 800,
      easing: 'easeOutExpo'
    });

    // Анимация при наведении
    const profileIcon = document.querySelector('.profile-icon');
    profileIcon.addEventListener('mouseenter', function() {
      anime({
        targets: profileIcon,
        scale: 1.1,
        color: '#FF6F61', // Цвет при наведении (RGB(255, 111, 97))
        duration: 300,
        easing: 'easeInOutSine'
      });
    });

    profileIcon.addEventListener('mouseleave', function() {
      anime({
        targets: profileIcon,
        scale: 1,
        color: 'white', // Возврат к начальному цвету
        duration: 300,
        easing: 'easeInOutSine'
      });
    });
  });