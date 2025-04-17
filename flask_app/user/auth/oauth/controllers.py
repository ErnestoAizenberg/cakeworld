from flask import flash, redirect, session, url_for


class OAuthController:
    def __init__(self, oauth_service: "OAuthService"):
        self.oauth_service = oauth_service

    def authorize(self, provider: str):
        """Перенаправляет пользователя на страницу авторизации провайдера."""
        try:
            auth_url = self.oauth_service.authorize(provider)
            print(auth_url)
            return redirect(auth_url)
        except ValueError as e:
            flash(str(e), "error")
            return redirect(url_for("auth.entry", mode="login"))

    def callback(self, provider: str, request_args: dict):
        """Обрабатывает ответ от провайдера и авторизует пользователя."""
        try:
            user_dto = self.oauth_service.callback(provider, request_args)
            session["user_id"] = user_dto.id
            flash("Login successful!", "success")
            return redirect(url_for("dashboard"))
        except ValueError as e:
            flash(str(e), "error")
            return redirect(url_for("auth.entry", mode="login"))
