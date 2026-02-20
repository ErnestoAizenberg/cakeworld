from flask import Flask

from .fubric import AppFactory

__all__ = ["app", "create_app"]


def create_app(
    config_class: str = "configs.development.DevelopmentConfig",
) -> Flask:
    """Factory function to create and configure the application"""
    factory: AppFactory = AppFactory()
    return factory.create_app(config_class)


if __name__ == "__main__":
    app: Flask = create_app()
