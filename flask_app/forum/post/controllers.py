from typing import List, Optional

from .dtos import PostDTO


class PostController:
    def __init__(self, post_service: "PostService"):
        self.post_service = post_service

    def view_post(self, post_id: int) -> Optional[PostDTO]:
        """Return the post with images."""
        return self.post_service.get_post_with_images(post_id)

    def create_post(
        self, form: "PostForm", user_id: int, topic_id: int
    ) -> Optional[PostDTO]:
        """Create a new post."""
        if form.validate():
            post_dto = PostDTO(
                title=form.title.data,
                content=form.content.data,
                user_id=user_id,
                topic_id=topic_id,
            )
            return self.post_service.create_post(post_dto)
        return None

    def reply_post(
        self, form: "ReplyForm", user_id: int, parent_post_id: int
    ) -> Optional[PostDTO]:
        """Create a reply to a post."""
        if form.validate():
            parent_post = self.post_service.get_post(parent_post_id)
            parent_post_topic_id = parent_post.topic_id
            post_dto = PostDTO(
                title=None,
                content=form.content.data,
                user_id=user_id,
                topic_id=parent_post_topic_id,
                post_id=parent_post_id,
            )
            return self.post_service.reply_post(post_dto)
        return None

    def edit_post(self, form: "PostForm", post_id: int) -> Optional[PostDTO]:
        """Edit an existing post."""
        if form.validate():
            post_dto = self.post_service.get_post_with_images(post_id)
            if not post_dto:
                return None

            updated_post_dto = PostDTO(
                title=form.title.data,
                content=form.content.data,
                user_id=post_dto.user_id,
                topic_id=post_dto.topic_id,
                post_id=post_dto.post_id,
                created=post_dto.created,
                images=post_dto.images,
                views=post_dto.views,
            )
            return self.post_service.update_post(updated_post_dto)

        return None

    def get_all_replies(self, post_id: int) -> List[PostDTO]:
        """Fetch all replies to a specific post."""
        return self.post_service.get_all_replies(post_id)

    def delete_post(self, post_id: int) -> bool:
        """Delete a post."""
        return self.post_service.delete_post(post_id)

    def add_view(self, post_id: int, user_id: int) -> bool:
        """Add a view to a post."""
        try:
            self.post_service.add_view(post_id, user_id)
            return True
        except ValueError:
            return False

    def add_images(self, post_id: int, images_list: List[str]) -> bool:
        """Add images to a post."""
        try:
            self.post_service.add_images(post_id, images_list)
            return True
        except ValueError:
            return False

    def set_content_html(self, post_id: int, html_content: str) -> bool:
        """Set HTML content for a post."""
        try:
            self.post_service.set_content_html(post_id, html_content)
            return True
        except ValueError:
            return False
