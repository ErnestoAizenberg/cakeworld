import os
import random

from PIL import Image, ImageDraw, ImageFont


class AvatarGenerator:
    def __init__(self, font_size=64, font_path=None):
        self.default_font_size = font_size
        self.default_font_path = font_path
        # Загружаем шрифт по умолчанию или указанный шрифт
        try:
            if self.default_font_path and os.path.exists(self.default_font_path):
                self.default_font = ImageFont.truetype(
                    self.default_font_path, self.default_font_size
                )
            else:
                self.default_font = ImageFont.load_default()
        except IOError:
            self.default_font = ImageFont.load_default()

    def random_color(self):
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def generate_avatar(
        self, name: str, save_path: str, font_size=None, font=None
    ) -> None:
        # Если размер шрифта не указан, используем значение по умолчанию
        if font_size is None:
            font_size = self.default_font_size

        # Если шрифт не указан, используем шрифт по умолчанию
        if font is None:
            font = self.default_font

        # Генерация рандомного фона
        background = Image.new("RGB", (128, 128), color=self.random_color())

        # Получение первой буквы имени
        initial = name[0].upper() if name else "U"  # 'U' как запасной вариант

        # Создание изображения с буквой имени
        draw = ImageDraw.Draw(background)

        # Получение размеров текста
        left, top, right, bottom = draw.textbbox((0, 0), initial, font=font)
        text_width = right - left
        text_height = bottom - top

        # Получение размеров изображения
        width, height = background.size

        # Расположение текста по центру
        text_position = ((width - text_width) / 2, (height - text_height) / 2)
        draw.text(text_position, initial, fill="white", font=font)

        # Сохранение сгенерированной аватарки
        background.save(save_path, format="PNG")


# Пример использования
if __name__ == "__main__":
    font_path = "static/fonts/DejaVuSans-Bold.ttf"
    avatar_generator = AvatarGenerator(font_path=font_path)
    avatar_generator.generate_avatar("5_оlmd", "avatar.png")
