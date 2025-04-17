import logging
from typing import List, Optional

from .dtos import PostDTO
from .repositories import PostRepository

logger = logging.getLogger(__name__)


class PostService:
    def __init__(self, post_repository: PostRepository):
        self.post_repository = post_repository

    def get_post_with_images(self, post_id: int) -> PostDTO:
        """Fetch post with associated images."""
        logger.info(f"Fetching post with images for post_id: {post_id}")
        return self.post_repository.get_post_with_images(post_id)

    def get_posts_by_user(self, user_id: int) -> List[PostDTO]:
        """Fetch posts created by the user."""
        logger.info(f"Fetching posts for user_id: {user_id}")
        return self.post_repository.get_posts_by_user(user_id)

    def get_all_posts(self, page: int = 1, per_page: int = 10) -> List[PostDTO]:
        """Fetch all posts with pagination."""
        logger.info(f"Fetching all posts, page: {page}, per_page: {per_page}")
        return self.post_repository.get_all(page=page, per_page=per_page)

    def get_all_replies(self, post_id: int) -> List[PostDTO]:
        """Fetch all replies to a specific post."""
        logger.info(f"Fetching replies for post_id: {post_id}")
        return self.post_repository.get_all(post_id=post_id)

    def get_post(self, post_id: int) -> PostDTO:
        """Get a post."""
        logger.info(f"Receiving post with the id: {post_id}")
        return self.post_repository.get(post_id)

    def create_post(self, post_dto: PostDTO) -> PostDTO:
        """Create a new post."""
        logger.info(f"Saving post: {post_dto}")
        return self.post_repository.save(post_dto)

    def update_post(self, post_dto: PostDTO) -> PostDTO:
        """Update an existing post."""
        logger.info(f"Updating post: {post_dto}")
        return self.post_repository.update(post_dto)

    def delete_post(self, post_id: int) -> bool:
        """Delete a post."""
        logger.info(f"Deleting post with post_id: {post_id}")
        return self.post_repository.delete(post_id)

    def reply_post(self, post_dto):
        return self.post_repository.save(post_dto)

    def add_view(self, post_id: int, user_id: int) -> None:
        """Add a view to a specific post by user_id."""
        logger.info(f"Adding view for post_id: {post_id} by user_id: {user_id}")
        post = self.post_repository.get(post_id)
        if post is None:
            logger.error("Post not found")
            raise ValueError("Post not found")

        post.views = post.views or []
        if user_id not in post.views:
            post.views.append(user_id)
            self.post_repository.save(post)

    def add_images(self, post_id: int, images_list: List[str]) -> None:
        """Add a list of images to a specific post."""
        logger.info(f"Adding images to post_id: {post_id}")
        post = self.post_repository.get(post_id)
        if post is None:
            logger.error("Post not found")
            raise ValueError("Post not found")

        post.images = images_list
        self.post_repository.save(post)

    def set_content_html(self, post_id: int, html_content: str) -> None:
        """Set sanitized HTML content for a post."""
        logger.info(f"Setting HTML content for post_id: {post_id}")
        from ..services.html_sanitizer import sanitize_html

        post = self.post_repository.get(post_id)
        if post is None:
            logger.error("Post not found")
            raise ValueError("Post not found")

        post.content = sanitize_html(html_content)
        self.post_repository.save(post)
