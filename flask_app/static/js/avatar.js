document.addEventListener('DOMContentLoaded', function() {
  // Close avatar menu
  const closeAvatarMenu = () => {
    const menu = document.getElementById('avatar-menu');
    if (menu) menu.style.display = 'none';
  };

  // Show the avatar menu
  const showAvatarMenu = (element) => {
    const menu = document.getElementById('avatar-menu');
    if (menu) {
      menu.style.display = 'block';
      const avatarImg = element.querySelector('.avatar');
      const largeAvatar = menu.querySelector('.large-avatar');

      // Ensure the correct avatar image path is used
      largeAvatar.src = avatarImg.src;
      largeAvatar.style.display = 'block'; // Ensure it's visible
    }
  };

  // Chat icon animation
  const chatIconClick = (icon) => {
    icon.style.transform = 'scale(1.2)';
    setTimeout(() => {
      icon.style.transform = 'scale(1)';
    }, 300);
  };

  // Assign global scope for event handlers
  window.closeAvatarMenu = closeAvatarMenu;
  window.showAvatarMenu = showAvatarMenu;
  window.chatIconClick = chatIconClick;
});