# flask_app/services/post_service.py
import logging
from typing import List, Optional

from ..repositories.post_repository import PostRepository
from .dtos.post_dto import PostDTO

logger = logging.getLogger(__name__)


class PostService:
    def __init__(self, post_repository: PostRepository):
        self.post_repository = post_repository

    def get_post_with_images(self, post_id: int) -> Optional[PostDTO]:
        logger.info(f"Fetching post with images for post_id: {post_id}")
        return self.post_repository.get_post_with_images(post_id)

    def get_posts_by_user(self, user_id: int) -> List[PostDTO]:
        logger.info(f"Fetching posts for user_id: {user_id}")
        return self.post_repository.get_posts_by_user(user_id)

    def get_all_posts(self, page: int = 1, per_page: int = 10) -> List[PostDTO]:
        logger.info(f"Fetching all posts, page: {page}, per_page: {per_page}")
        return self.post_repository.get_all(page=page, per_page=per_page)

    def get_all_replies(self) -> List[PostDTO]:
        logger.info("Fetching all replies")
        return self.post_repository.get_all_replies()

    def save(self, post_dto: PostDTO) -> PostDTO:
        logger.info(f"Saving post: {post_dto}")
        return self.post_repository.save(post_dto)

    def update(self, post_dto: PostDTO) -> PostDTO:
        logger.info(f"Updating post: {post_dto}")
        return self.post_repository.update(post_dto)

    def delete(self, post_id: int) -> bool:
        logger.info(f"Deleting post with post_id: {post_id}")
        return self.post_repository.delete(post_id)

    def get_username_by_id(self, user_id: int) -> str:
        logger.info(f"Fetching username for user_id: {user_id}")
        return self.post_repository.get_username_by_id(user_id)

    def get_post_title(self, post_id: int) -> str:
        logger.info(f"Fetching title for post_id: {post_id}")
        return self.post_repository.get_post_title(post_id)

    def count_user_posts(self, user_id: int) -> int:
        logger.info(f"Counting posts for user_id: {user_id}")
        return self.post_repository.count_user_posts(user_id)

    def add_view(self, post_id: int, user_id: int) -> None:
        logger.info(f"Adding view for post_id: {post_id} by user_id: {user_id}")
        post = self.post_repository.get(post_id)
        if not post:
            logger.error("Post not found")
            raise ValueError("Post not found")

        if post.views is None:
            post.views = []
        if user_id not in post.views:
            post.views.append(user_id)
            self.post_repository.save(post)

    def add_images(self, post_id: int, images_list: List[str]) -> None:
        logger.info(f"Adding images to post_id: {post_id}")
        post = self.post_repository.get(post_id)
        if not post:
            logger.error("Post not found")
            raise ValueError("Post not found")

        post.images = images_list
        self.post_repository.save(post)

    def set_content_html(self, post_id: int, html_content: str) -> None:
        logger.info(f"Setting HTML content for post_id: {post_id}")
        from ..services.html_sanitizer import sanitize_html

        post = self.post_repository.get(post_id)
        if not post:
            logger.error("Post not found")
            raise ValueError("Post not found")

        post.content = sanitize_html(html_content)
        self.post_repository.save(post)
