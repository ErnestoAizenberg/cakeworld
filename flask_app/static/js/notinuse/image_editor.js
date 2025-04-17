  const imageInput = document.getElementById('imageInput');
  const imagePreviews = document.getElementById('imagePreviews');
  const messageForm = document.getElementById('messageForm');

  // Обработка выбора изображений
  imageInput.addEventListener('change', (event) => {
    const files = event.target.files;
    for (const file of files) {
      const reader = new FileReader();
      reader.onload = (e) => {
        const previewItem = document.createElement('div');
        previewItem.classList.add('image-preview-item');

        const img = document.createElement('img');
        img.src = e.target.result;

        const removeBtn = document.createElement('button');
        removeBtn.classList.add('remove-btn');
        removeBtn.innerHTML = '×';
        removeBtn.addEventListener('click', () => {
          previewItem.remove();
        });

        previewItem.appendChild(img);
        previewItem.appendChild(removeBtn);
        imagePreviews.appendChild(previewItem);

        // Открыть редактор при клике на изображение
        img.addEventListener('click', () => openImageEditor(img.src));
      };
      reader.readAsDataURL(file);
    }
  });
  // Функция для открытия редактора изображений
  function openImageEditor(imageSrc) {
    const editor = document.createElement('div');
    editor.style.position = 'fixed';
    editor.style.top = '0';
    editor.style.left = '0';
    editor.style.width = '100%';
    editor.style.height = '100%';
    editor.style.backgroundColor = 'rgba(0, 0, 0, 0.8)';
    editor.style.display = 'flex';
    editor.style.justifyContent = 'center';
    editor.style.alignItems = 'center';
    editor.style.zIndex = '1000';

    const img = document.createElement('img');
    img.src = imageSrc;
    img.style.maxWidth = '90%';
    img.style.maxHeight = '90%';
    img.style.borderRadius = '10px';

    editor.appendChild(img);
    document.body.appendChild(editor);

    // Закрыть редактор при клике
    editor.addEventListener('click', () => {
      document.body.removeChild(editor);
    });
  }