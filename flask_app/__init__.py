from flask import Flask

from .fubric import AppFactory


def create_app(config_class: str = "instance.config.Config") -> Flask:
    """Factory function to create and configure the application"""
    factory = AppFactory()
    return factory.create_app(config_class)


if __name__ == "__main__":
    app = create_app()
