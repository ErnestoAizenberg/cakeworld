// Logo animation
new Vivus('minecraft-logo', {
  duration: 200,
  type: 'delayed',
  animTimingFunction: Vivus.EASE
});

// Button hover animation
document.querySelectorAll('.btn').forEach(button => {
  button.addEventListener('mouseover', () => {
    anime({
      targets: button,
      scale: 1.1,
      duration: 500
    });
  });
});

// Card hover animation
document.querySelectorAll('.card').forEach(card => {
  card.addEventListener('mouseover', () => {
    anime({
      targets: card,
      scale: 1.05,
      duration: 300
    });
  });
});