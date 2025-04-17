from typing import List, Optional, Tuple

from .dtos import PostDTO


class PostController:
    def __init__(
        self,
        post_service: "PostService",
        # PostForm: 'FlaskForm',
        # ReplyForm: 'FlaskForm'
    ):
        self.post_service = post_service
        # self.post_form = post_form
        # self.reply_form = reply_form

    def view_post(self, post_id: int) -> Optional[PostDTO]:
        """Возвращает пост с изображениями."""
        return self.post_service.get_post_with_images(post_id)

    def create_post(
        self, form: "PostForm", user_id: int, topic_id: int
    ) -> Tuple[bool, str, Optional[PostDTO]]:
        """Создает новый пост."""
        if form.validate():
            post_dto = PostDTO(
                id=None,
                title=form.title.data,
                content=form.content.data,
                user_id=user_id,
                topic_id=topic_id,
                post_id=None,
                created=None,
                images=None,
                views=None,
            )
            return self.post_service.create_post(post_dto)
        return False, "Invalid form data", None

    def reply_post(
        self, form: "ReplyForm", user_id: int, post_id: int
    ) -> Tuple[bool, str, Optional[PostDTO]]:
        """Создает ответ на пост."""
        if form.validate():
            post_dto = PostDTO(
                id=None,
                title=None,
                content=form.content.data,
                user_id=user_id,
                topic_id=None,  # Будет установлено в сервисе
                post_id=post_id,
                created=None,
                images=None,
                views=None,
            )
            return self.post_service.reply_post(post_dto)
        return False, "Invalid form data", None

    def edit_post(
        self, form: "PostForm", post_id: int
    ) -> Tuple[bool, str, Optional[PostDTO]]:
        """Редактирует пост."""
        if form.validate():
            post_dto = self.post_service.get_post_with_images(post_id)
            if not post_dto:
                return False, "Post not found", None

            updated_post_dto = PostDTO(
                id=post_dto.id,
                title=form.title.data,
                content=form.content.data,
                user_id=post_dto.user_id,
                topic_id=post_dto.topic_id,
                post_id=post_dto.post_id,
                created=post_dto.created,
                images=post_dto.images,
                views=post_dto.views,
            )
            return self.post_service.edit_post(updated_post_dto)
        return False, "Invalid form data", None

    def delete_post(self, post_id: int) -> Tuple[bool, str]:
        """Удаляет пост."""
        return self.post_service.delete_post(post_id)

    def add_view(self, post_id: int, user_id: int) -> Tuple[bool, str]:
        """Добавляет просмотр поста пользователем."""
        return self.post_service.add_view(post_id, user_id)

    def add_images(self, post_id: int, images_list: List[str]) -> Tuple[bool, str]:
        """Добавляет изображения к посту."""
        return self.post_service.add_images(post_id, images_list)

    def set_content_html(self, post_id: int, html_content: str) -> Tuple[bool, str]:
        """Устанавливает очищенное HTML-содержимое."""
        return self.post_service.set_content_html(post_id, html_content)
