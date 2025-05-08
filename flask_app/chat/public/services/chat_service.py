import json
import logging
from dataclasses import asdict
from typing import List, Optional

import redis

from flask_app.chat.message.dtos import MessageDTO
from flask_app.chat.public.dtos import ChatDTO
from flask_app.user.chat_user.dtos import ChatUserDTO
from flask_app.chat.exceptions import *


class CacheKeys:
    """Namespace for Redis key patterns."""

    CHAT_BY_ID = "chat:{}"
    CHAT_BY_URL = "chat:url:{}"
    DIRECT_CHAT_BY_USERS = "chat:direct:{}:{}"
    USER_CHATS = "user:{}:chats"
    CHAT_USERS = "chat:{}:users"


class CacheTTL:
    """Cache expiration times."""

    SHORT = 300  # 5 minutes
    LONG = 3600  # 1 hour
    DIRECT_CHAT = 86400  # 24 hours for direct chats


class ChatService:
    def __init__(
        self, chat_repo, chat_user_repo, message_repo, redis_client: redis.Redis
    ):
        self.chat_repo = chat_repo
        self.chat_user_repo = chat_user_repo
        self.message_repo = message_repo
        self.redis = redis_client
        self.logger = logging.getLogger(__name__)

    # --------------------------
    # Core Caching Infrastructure
    # --------------------------

    def _cache_get(self, key: str) -> Optional[dict]:
        """Get JSON data from Redis with proper error handling."""
        try:
            if data := self.redis.get(key):
                return json.loads(data)
        except (json.JSONDecodeError, redis.RedisError) as e:
            self.logger.warning(f"Cache read failed for key {key}: {str(e)}")
        return None

    def _cache_set(self, key: str, data: dict, ttl: int) -> bool:
        """Set JSON data in Redis with proper error handling."""
        try:
            self.redis.setex(key, ttl, json.dumps(data))
            return True
        except (TypeError, redis.RedisError) as e:
            self.logger.warning(f"Cache write failed for key {key}: {str(e)}")
            return False

    def _cache_delete(self, *keys: str) -> None:
        """Delete cache keys with error handling."""
        try:
            self.redis.delete(*keys)
        except redis.RedisError as e:
            self.logger.warning(f"Cache delete failed for keys {keys}: {str(e)}")

    def _invalidate_chat_cache(self, chat_id: int, url_name: str) -> None:
        """Invalidate all cache entries related to a chat."""
        keys = [
            CacheKeys.CHAT_BY_ID.format(chat_id),
            CacheKeys.CHAT_BY_URL.format(url_name),
            CacheKeys.CHAT_USERS.format(chat_id),
        ]
        self._cache_delete(*keys)

    # --------------------------
    # Chat Operations with Caching
    # --------------------------

    def get_chat_by_id(
        self, chat_id: int, prefetch_users: bool = True
    ) -> Optional[ChatDTO]:
        """Get chat by ID with caching and optional user prefetch."""
        cache_key = CacheKeys.CHAT_BY_ID.format(chat_id)

        # Try cache first
        if cached := self._cache_get(cache_key):
            chat = ChatDTO(**cached)

            # Prefetch users if requested (cache-ahead pattern)
            if prefetch_users and not self._cache_get(
                CacheKeys.CHAT_USERS.format(chat_id)
            ):
                self._prefetch_chat_users(chat_id)

            return chat

        # Cache miss - fetch from DB
        chat = self.chat_repo.get(chat_id)
        if chat:
            self._cache_set(cache_key, asdict(chat), CacheTTL.LONG)

            # Predict and cache likely needed data
            if prefetch_users:
                self._prefetch_chat_users(chat_id)

        return chat

    def get_chat_by_url(self, url_name: str) -> Optional[ChatDTO]:
        """Get chat by URL name with caching."""
        cache_key = CacheKeys.CHAT_BY_URL.format(url_name)

        if cached := self._cache_get(cache_key):
            return ChatDTO(**cached)

        chat = self.chat_repo.get_chat_by_url(url_name)
        if chat:
            self._cache_set(cache_key, asdict(chat), CacheTTL.LONG)
            self._cache_set(
                CacheKeys.CHAT_BY_ID.format(chat.id), asdict(chat), CacheTTL.LONG
            )
        return chat

    def create_chat(self, title: str, url_name: str, **kwargs) -> ChatDTO:
        """Create new chat with cache invalidation."""
        chat = self.chat_repo.save(ChatDTO(title=title, url_name=url_name, **kwargs))
        # self._invalidate_user_chats_cache(chat.creator_id)
        return chat

    # --------------------------
    # Direct Chat Operations
    # --------------------------

    def get_or_create_direct_chat(self, user1_id: int, user2_id: int) -> ChatDTO:
        """Get or create direct chat with specialized caching."""
        # Генерация ключа кеша
        cache_key = CacheKeys.DIRECT_CHAT_BY_USERS.format(
            min(user1_id, user2_id), max(user1_id, user2_id)
        )

        try:
            # Проверка кеша
            if cached := self._cache_get(cache_key):
                return ChatDTO(
                    cached
                )  # Удостоверьтесь, что cached имеет правильную структуру
            # Проверка существующего чата
            url_name = self._generate_direct_chat_url(user1_id, user2_id)
            if chat := self.get_chat_by_url(url_name):
                self._cache_set(cache_key, asdict(chat), CacheTTL.DIRECT_CHAT)
                return chat
            # Создание нового прямого чата
            title = f"Direct Chat ({user1_id} & {user2_id})"
            chat = self.create_chat(title=title, url_name=url_name, is_private=True)
            # Создание пользователей чата
            self.create_chat_user(user1_id, chat.id)
            self.create_chat_user(user2_id, chat.id)
            # Установка кеша
            self._cache_set(cache_key, asdict(chat), CacheTTL.DIRECT_CHAT)
            return chat

        except Exception as e:
            self.logger.error(f"Error in get_or_create_direct_chat: {str(e)}")
            raise ChatCreationError("Could not get or create direct chat")

    # --------------------------
    # User-Chat Relationships
    # --------------------------

    def _prefetch_chat_users(self, chat_id: int) -> None:
        """Prefetch and cache chat users (cache-ahead pattern)."""
        users = self.chat_user_repo.get_all(chat_id=chat_id)
        if users:
            self._cache_set(
                CacheKeys.CHAT_USERS.format(chat_id),
                [asdict(u) for u in users],
                CacheTTL.SHORT,
            )

    def get_chat_users(self, chat_id: int) -> List[ChatUserDTO]:
        """Get chat users with caching."""
        cache_key = CacheKeys.CHAT_USERS.format(chat_id)

        if cached := self._cache_get(cache_key):
            return [ChatUserDTO(**u) for u in cached]

        users = self.chat_user_repo.get_chat_users(chat_id)
        if users:
            self._cache_set(cache_key, [asdict(u) for u in users], CacheTTL.SHORT)
        return users

    def create_chat_user(self, user_id: int, chat_id: int) -> ChatUserDTO:
        """Add user to chat with cache invalidation."""
        chat_user = self.chat_user_repo.save(
            ChatUserDTO(user_id=user_id, chat_id=chat_id)
        )

        # Invalidate relevant caches
        self._cache_delete(
            CacheKeys.USER_CHATS.format(user_id), CacheKeys.CHAT_USERS.format(chat_id)
        )

        # Prefetch updated data
        self.get_user_chats(user_id)

        print("[DEBUG] chat_user: ", chat_user)
        return chat_user

    # --------------------------
    # User-Centric Operations
    # --------------------------

    def _invalidate_user_chats_cache(self, user_id: int) -> None:
        """Invalidate all cache entries related to user's chats."""
        self._cache_delete(CacheKeys.USER_CHATS.format(user_id))

    def get_user_chats(self, user_id: int) -> List[ChatDTO]:
        """Get user's chats with write-through caching."""
        cache_key = CacheKeys.USER_CHATS.format(user_id)

        if cached := self._cache_get(cache_key):
            return [ChatDTO(**c) for c in cached]

        chats = self.chat_user_repo.get_user_chats(user_id)
        if chats:
            self._cache_set(cache_key, [asdict(c) for c in chats], CacheTTL.LONG)

            # Prefetch chat details (cache-ahead)
            for chat in chats:
                self._cache_set(
                    CacheKeys.CHAT_BY_ID.format(chat.id), asdict(chat), CacheTTL.LONG
                )
        return chats

    def is_user_in_chat(self, user_id: int, chat_id: int) -> bool:
        """Check user membership with cache optimization."""
        # First try the cached user chats
        if cached_chats := self._cache_get(CacheKeys.USER_CHATS.format(user_id)):
            return any(c["id"] == chat_id for c in cached_chats)

        # Fallback to direct check
        return bool(self.chat_user_repo.get_chat_user(user_id, chat_id))

    # --------------------------
    # Message Operations
    # --------------------------

    def get_chat_messages(self, chat_id: int, limit: int = 50) -> List[MessageDTO]:
        """Get chat messages with cache-ahead pattern."""
        # In a real implementation, you might cache message threads
        messages = self.message_repo.get_chat_messages(chat_id, limit)

        # Prefetch likely needed user data
        user_ids = {m.user_id for m in messages}
        for uid in user_ids:
            if not self._cache_get(f"user:{uid}"):
                # Would normally prefetch user profiles here
                pass

        return messages

    def get_chat_by_users(self, user1_id: int, user2_id: int) -> Optional[ChatDTO]:
        """Finds direct chat between two users."""
        try:
            url_name = self._generate_direct_chat_url(user1_id, user2_id)
            return self.chat_repo.get_chat_by_url(url_name)
        except Exception as e:
            self.logger.error(f"Error finding chat by users: {str(e)}")
            return None

    def _generate_direct_chat_url(self, user1_id: int, user2_id: int) -> str:
        """Generates consistent URL name for direct chats."""
        if not all(isinstance(i, int) and i > 0 for i in (user1_id, user2_id)):
            raise ValidationError("User IDs must be positive integers")
        return f"direct_{min(user1_id, user2_id)}_{max(user1_id, user2_id)}"

    def create_direct_chat(
        self, user1_id: int, user2_id: int, title: str = None
    ) -> ChatDTO:
        """Creates a direct chat between two users with automatic ChatUser creation.

        Args:
            user1_id: First user ID
            user2_id: Second user ID
            title: Optional custom title (defaults to "User1 & User2")

        Returns:
            Created ChatDTO

        Raises:
            ChatCreationError: If any step fails
        """
        try:
            # Validate input
            if user1_id == user2_id:
                raise ValidationError("Cannot create direct chat with same user")

            # Generate consistent URL name
            url_name = self._generate_direct_chat_url(user1_id, user2_id)

            # Check if chat already exists
            existing_chat = self.chat_repo.get_chat_by_url(url_name)
            if existing_chat:
                print("[DEBUG] Returning exiting chat")
                return existing_chat

            # Create default title if none provided
            if not title:
                user1 = f"User-{user1_id}"
                user2 = f"User-{user2_id}"
                title = f"{user1} & {user2}"

            # Create the chat
            chat_dto = self.create_chat(title=title, url_name=url_name, is_private=True)

            # Add both users to the chat
            self.create_chat_user(user1_id, chat_dto.id)
            self.create_chat_user(user2_id, chat_dto.id)

            return chat_dto

        except Exception as e:
            self.logger.error(f"Failed to create direct chat: {str(e)}")
            raise ChatCreationError(f"Could not create direct chat: {str(e)}")
