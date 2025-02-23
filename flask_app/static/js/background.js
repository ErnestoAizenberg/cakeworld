// Two.js for homepage background
const two = new Two({ width: window.innerWidth, height: 400 }).appendTo(document.getElementById('hero-background'));
const blocks = [];
for (let i = 0; i < 20; i++) {
  const block = two.makeRectangle(Math.random() * two.width, Math.random() * two.height, 50, 50);
  block.fill = '#8B4513';
  blocks.push(block);
}
two.bind('update', () => {
  blocks.forEach(block => {
    block.translation.x += Math.random() * 2 - 1;
    block.translation.y += Math.random() * 2 - 1;
  });
}).play();

// Paper.js for admin panel background
paper.install(window);
window.onload = () => {
  const canvas = document.getElementById('admin-background');
  paper.setup(canvas);
  const path = new Path.Rectangle(new Point(50, 50), new Size(700, 300));
  path.fillColor = '#8B4513';
  path.onFrame = () => {
    path.rotate(1);
  };
};