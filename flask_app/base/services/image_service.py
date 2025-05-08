from io import BytesIO

from PIL import Image


class ImageService:
    def process_image(self, img_data: BytesIO, full_image_path: str) -> None:
        with Image.open(img_data) as img:
            img.save(full_image_path)
