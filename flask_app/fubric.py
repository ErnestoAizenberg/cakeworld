import os
import logging
from typing import Optional

from flask import Flask
from redis import Redis
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect


class AppFactory:
    def __init__(self):
        self.app: Optional[Flask] = None
        self.db: Optional[SQLAlchemy] = None
        self.redis_client: Optional[Redis] = None
        self.socketio: Optional[SocketIO] = None
        self.csrf: Optional[CSRFProtect] = None
        self._components = {
            "forms": {},
            "repositories": {},
            "services": {},
            "controllers": {},
        }
        self.logger = logging.getLogger(__name__)

    def create_app(
        self,
        config_class: str = "configs.development.DevelopmentConfig",
        # mail_config: Dict,
    ) -> Flask:
        self.app = Flask(__name__, template_folder="templates", static_folder="static")

        if config_class:
            self.app.config.from_object(config_class)
        elif os.environ.get("FLASK_ENV") == "production":
            self.app.config.from_object("config.ProductionConfig")
        else:
            self.app.config.from_object("config.DevelopmentConfig")
        
        use_redis = False
        if use_redis:
            self.redis_client = (
                Redis.from_url(self.app.config["REDIS_URL"])
                if self.app.config.get("REDIS_URL")
                else None
            )

        self._init_templates()
        self._init_extensions()
        self._init_components()
        self._register_routes()
        self._configure_socketio()

        return self.app

    def _init_extensions(self):
        """Initialize Flask extensions"""
        from .extensions import csrf, db, socketio

        self.db = db
        self.socketio = socketio
        self.csrf = csrf
        
        if self.app:
            db.init_app(self.app)
            socketio.init_app(self.app)
        else:
            raise ValueError("Application is None")
        
        if csrf:
            csrf.init_app(self.app)

    def _init_templates(self):
        template_dir = os.path.join(os.path.dirname(__file__), "templates")
        self.logger.debug(f"template_dir: {template_dir}")

        paths = [
            "flask_app/user/templates",
            "forum/templates",
            "flask_app/game/templates",
            "flask_app/chat/templates",
            "flask_app/chat/public/templates",
            "flask_app/chat/direct/templates",
            "flask_app/chat/message/templates",
            "flask_app/forum/templates",
            "flask_app/forum/post/templates",
            "flask_app/forum/category/templates",
            "flask_app/game/templates",
            "flask_app/user/notification/templates",
            "flask_app/user/templates",
            "flask_app/chat/templates",
            "flask_app/website/templates",
            "flask_app/website/editing/templates",
            "flask_app/website/statistics/templates",
            "flask_app/forum/topic/templates",
            "flask_app/forum/post/templates",
            "flask_app/user/auth/templates",
            "flask_app/user/profile/templates",
        ]

        for path in paths:
            if self.app:
                if self.app.jinja_loader:
                    self.app.jinja_loader.searchpath.append(path)
                else:
                    raise RuntimeError("Jinja Loader is not set")
            else:
                raise RuntimeError("Application instance is not set")

        print("[DEBUG] templates are registered")

    def _init_components(self):
        """Initialize all application components"""
        self._init_forms()
        self._init_repositories()
        self._init_services()
        self._init_controllers()
        self._confugure_game()

    def _init_forms(self):
        """Initialize all forms"""
        from .chat.public.forms import ChatForm
        from .forum.category.forms import CategoryForm
        from .forum.post.forms import PostForm, ReplyForm
        from .forum.topic.forms import TopicForm
        from .website.editing.forms import ServerForm

        self._components["forms"] = {
            "category": CategoryForm,
            "post": PostForm,
            "reply": ReplyForm,
            "server": ServerForm,
            "topic": TopicForm,
            "chat": ChatForm,
        }

    def _init_repositories(self):
        """Initialize all repositories"""
        from .chat.message.reaction.repositories import MessageReactionRepository
        from .chat.message.repositories import MessageRepository
        from .chat.public.repositories import ChatRepository
        from .forum.category.repositories import CategoryRepository
        from .forum.post.repositories import PostRepository
        from .forum.topic.repositories import TopicRepository
        from .user.ban.repositories import BannedUserRepository
        from .user.chat_user.repositories import ChatUserRepository
        from .user.notification.repositories import NotificationRepository
        from .user.repositories import UserRepository

        if not self.db:
            raise RuntimeError("DB is not set")
        
        self._components["repositories"] = {
            "user": UserRepository(self.db.session),
            "topic": TopicRepository(self.db.session),
            "category": CategoryRepository(self.db.session),
            "banned_user": BannedUserRepository(self.db.session),
            "post": PostRepository(self.db.session),
            "notification": NotificationRepository(self.db.session),
            "message_reaction": MessageReactionRepository(self.db.session),
            "chat": ChatRepository(self.db.session),
            "chat_user": ChatUserRepository(self.db.session),
            "message": MessageRepository(self.db.session),
        }

    def _init_services(self):
        """Initialize all services"""
        from .base.services import ImageService
        from .chat.direct.services import DirectChatService
        from .chat.message.reaction.services import ReactionService
        from .chat.message.services import MessageService
        from .chat.public.services import ChatAvatarService, ChatService
        from .forum.category.services import CategoryService
        from .forum.topic.services import TopicService
        from .forum.post.services import PostService
        from .user.auth.oauth.services import OAuthService
        from .user.auth.services import AuthService, EmailService
        from .user.ban.services import BanService
        from .user.notification.services import NotificationService
        from .user.profile.avatar.generators import AvatarGenerator
        from .user.profile.avatar.services import AvatarService
        from .user.profile.services import ProfileService
        from .user.services import UserService

        repos = self._components["repositories"]
        image_service = ImageService()
        avatar_generator = AvatarGenerator(font_path="static/fonts/DejaVuSans-Bold.ttf")
        profile_service = ProfileService(
            repos["user"],
        )
        avatar_service = AvatarService(
            user_repo=repos["user"],
            image_service=image_service,
            avatar_generator=avatar_generator,
            redis_client=self.redis_client,
        )
        user_service = UserService(repos["user"])
        if not self.app:
            raise RuntimeError("Application instance is not set")

        if not self.app.config:
            raise RuntimeError("Config instance is not set")

        email_service = EmailService(
            smtp_server=self.app.config.get("MAIL_SERVER", ""),
            smtp_port=self.app.config.get("MAIL_PORT", ""),
            smtp_username=self.app.config.get("MAIL_USERNAME", ""),
            smtp_password=self.app.config.get("MAIL_PASSWORD", ""),
            sender=self.app.config.get("MAIL_USERNAME", ""),
            use_tls=self.app.config.get("MAIL_USE_TLS", ""),
        )
        auth_service = AuthService(repos["user"], email_service)
        oauth_service = OAuthService(repos["user"], auth_service)
        notification_service = NotificationService(repos["notification"])
        ban_service = BanService(repos["banned_user"])
        post_service = PostService(repos["post"])
        category_service = CategoryService(
            repos["category"],
            repos["topic"],
        )
        topic_service = TopicService(
            topic_repository=repos["topic"],
            redis_client=self.redis_client
        )

        chat_avatar_service = ChatAvatarService(
            image_service,
            repos["chat"],
            avatar_generator,
        )

        message_reaction_service = ReactionService(repos["message_reaction"])
        message_service = MessageService(repos["message"])
        chat_service = ChatService(
            repos["chat"],
            repos["chat_user"],
            repos["message"],
            redis_client=self.redis_client,
        )
        direct_chat_service = DirectChatService(
            chat_service,
            message_service,
        )
        self._components["services"] = {
            "email": email_service,
            "auth": auth_service,
            "profile": profile_service,
            "avatar": avatar_service,
            "ban": ban_service,
            "oauth": oauth_service,
            "user": user_service,
            "category": category_service,
            "topic": topic_service,
            "post": post_service,
            "notification": notification_service,
            "message_reaction": message_reaction_service,
            "chat": chat_service,
            "message": message_service,
            "chat_avatar": chat_avatar_service,
            "direct_chat": direct_chat_service,
        }

    def _init_controllers(self):
        """Initialize all controllers"""
        from .chat.message.reaction.controllers import MessageReactionController
        from .chat.public.controllers import ChatController
        from .forum.category.controllers import CategoryController
        from .forum.topic.controllers import TopicController
        from .forum.post.controllers import PostController
        from .user.auth.controllers import AuthController
        from .user.ban.controllers import BanController
        from .user.controllers import UserController
        from .user.notification.controllers import NotificationController
        from .user.profile.controllers import ProfileController
        from .website.statistics.controllers import SiteStatsController

        services = self._components["services"]
        repos = self._components["repositories"]
        forms = self._components["forms"]

        profile_controller = ProfileController(
            profile_service=services["profile"],
            avatar_service=services["avatar"],
            user_repo=repos["user"],
            chat_user_repo=repos["chat_user"],
        )
        category_controller = CategoryController(
            services["category"],
            forms["category"],
        )
        topic_controller = TopicController(services["topic"])
        chat = ChatController(
            services["user"],
            services["chat"],
            services["message"],
        )
        notification = NotificationController(
            services["notification"],
        )
        auth = AuthController(
            services["auth"],
            services["notification"],
        )
        site_stats = SiteStatsController(
            self.db.session,
        )
        message_reaction = MessageReactionController(services["message_reaction"])
        post = PostController(services["post"])
        ban = BanController(services["ban"])
        user = UserController(services["user"])

        self._components["controllers"] = {
            "topic": topic_controller,
            "category": category_controller,
            "auth": auth,
            "user": user,
            "ban": ban,
            "post": post,
            "notification": notification,
            "profile": profile_controller,
            "chat": chat,
            "site_stats": site_stats,
            "message_reaction": message_reaction,
        }

    def _register_routes(self):
        if not self.app:
            raise RuntimeError("Can not regiter routes as application instance is not set")
        
        """Register all application routes"""
        from .base.routes import setup_request_hooks
        from .chat.direct.routes import DirectChatRoutes
        from .chat.message.reaction.routes import configure_reaction_routes
        from .chat.public.routes import configure_chat_routes
        from .forum.category.routes import configure_topic_category_routes
        from .forum.post.routes import configure_post_routes
        from .user.auth.oauth.routes import configure_oauth_routes
        from .user.auth.routes import init_auth_routes
        from .user.ban.routes import configure_ban_routes
        from .user.notification.routes import configure_notification_routes
        from .user.profile.routes import configure_profile_routes
        from .user.routes import configure_user_routes
        from .website.editing.routes import configure_editsite_routes
        from .website.statistics.routes import configure_site_statistics
        from .website.view.routes import configure_pages
        from .forum.topic.routes import configure_topic_routes

        controllers = self._components["controllers"]
        services = self._components["services"]
        forms = self._components["forms"]

        # Basic routes
        setup_request_hooks(self.app, services["user"], services["profile"])
        # configure_cache_routes(self.app)
        # configure_exception_routes(self.app)
        configure_pages(self.app)

        # Auth routes
        init_auth_routes(self.app, controllers["auth"])
        configure_oauth_routes(self.app, services["oauth"])

        # User management routes
        configure_user_routes(self.app, controllers["user"])
        configure_profile_routes(
            self.app,
            controllers["profile"],
        )
        configure_ban_routes(self.app, controllers["ban"])

        # Forum routes
        configure_post_routes(
            app=self.app,
            post_controller=controllers["post"],
            PostForm=forms["post"],
            ReplyForm=forms["reply"]
        )
        configure_topic_category_routes(
            app=self.app,
            category_controller=controllers["category"],
            CategoryForm=forms["category"],
        ) 
        configure_topic_routes(self.app, controllers["topic"])
        configure_reaction_routes(self.app, controllers["message_reaction"])

        # Chat routes
        if not self.socketio:
            raise RuntimeError("Can not register chat routes as socketio instance is not set")
        
        configure_chat_routes(
            self.app,
            self.socketio,
            forms["chat"],
            controllers["chat"],
            services["chat"],
        )
        # Other routes

        ###performance_checker = SitePerformanceChecker(self.app)# danger!!!
        configure_site_statistics(self.app, controllers["site_stats"])
        configure_notification_routes(self.app, controllers["notification"])
        configure_editsite_routes(self.app, forms["server"])
        DirectChatRoutes(
            app=self.app,
            socketio=self.socketio,
            user_service=services["user"],
            direct_chat_service=services["direct_chat"],
        )

    def _confugure_game(self):
        if not self.db:
            raise RuntimeError("Can not configure game, db is not set")
        
        from .game.banner.repositories import BannerRepository
        from .game.banner.services import BannerService
        from .game.currency.repositories import CurrencyRepository
        from .game.currency.services import CurrencyService
        from .game.inventory.repositories import InventoryItemRepository
        from .game.inventory.services import InventoryItemService
        from .game.item.repositories import StoreItemRepository
        from .game.item.services import StoreItemService
        from .game.prayer.services import PrayerService
        from .game.prayer.user_prayer.repositories import UserPrayRepository

        store_item_repository = StoreItemRepository(self.db.session)
        banner_repository = BannerRepository(self.db.session)
        user_pray_repository = UserPrayRepository(self.db.session)
        inventory_item_repository = InventoryItemRepository(self.db.session)
        currency_repository = CurrencyRepository(self.db.session)

        store_item_service = StoreItemService(store_item_repository)
        inventory_service = InventoryItemService(inventory_item_repository)
        banner_service = BannerService(banner_repository)
        currency_service = CurrencyService(currency_repository)
        prayer_service = PrayerService(
            prayer_repository=user_pray_repository,
            item_service=store_item_service,
            currency_repository=currency_repository,
        )

        from .game.routes import DataReciver, init_game

        data_reciver = DataReciver(
            currency_service,
            banner_service,
            inventory_service,
        )
        init_game(self.app, data_reciver, prayer_service, inventory_service)

    def _configure_socketio(self):
        """Configure SocketIO handlers"""
        # from .chat.direct.routes import configure_direct_chating
        from .chat.message.reaction.routes import configure_message_reaction_routes
        from .chat.public.routes import configure_real_time_chating

        services = self._components["services"]
        controllers = self._components["controllers"]

        configure_message_reaction_routes(controllers["message_reaction"])
        """configure_direct_chating(
            self.app,
            self.socketio,
            services['user'],
            services['direct_chat']
        )"""
        configure_real_time_chating(
            self.app,
            self.socketio,
            self.csrf,
            services["chat"],
            services["message"],
            services["chat_avatar"],
        )


def create_app(config_class: str = "instance.config.Config") -> Flask:
    """Factory function to create and configure the application"""
    factory = AppFactory()
    return factory.create_app(config_class)
