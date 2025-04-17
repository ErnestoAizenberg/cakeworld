# flask_app/services/oauth_service.py
import secrets
from urllib.parse import urlencode

import requests
from flask import current_app, session, url_for
from requests.exceptions import SSLError

from .dtos import UserDTO


class OAuthService:
    def __init__(self, user_repo: "UserRepository", auth_service: "AuthService"):
        self.user_repo = user_repo
        self.auth_service = auth_service

    def authorize(self, provider: str) -> str:
        """Генерирует URL для перенаправления на страницу авторизации провайдера."""
        provider_data = current_app.config["OAUTH2_PROVIDERS"].get(provider)
        if not provider_data:
            raise ValueError("Provider not found")

        session["oauth2_state"] = secrets.token_urlsafe(16)

        qs = urlencode(
            {
                "client_id": provider_data["client_id"],
                "redirect_uri": url_for(
                    "oauth2_callback", provider=provider, _external=True
                ),
                "response_type": "code",
                "scope": " ".join(provider_data["scopes"]),
                "state": session["oauth2_state"],
            }
        )

        return provider_data["authorize_url"] + "?" + qs

    def callback(self, provider: str, request_args: dict) -> UserDTO:
        """Обрабатывает ответ от провайдера и авторизует пользователя."""
        provider_data = current_app.config["OAUTH2_PROVIDERS"].get(provider)
        if not provider_data:
            raise ValueError("Provider not found")

        if "error" in request_args:
            raise ValueError(f"OAuth error: {request_args.get('error')}")

        if (
            "oauth2_state" not in session
            or request_args.get("state") != session["oauth2_state"]
        ):
            raise ValueError("Invalid state parameter")

        session.pop("oauth2_state")

        if "code" not in request_args:
            raise ValueError("Authorization code not found")

        oauth2_token = self._get_access_token(provider_data, request_args["code"])
        user_info = self._get_user_info(provider_data, oauth2_token)
        email = provider_data["userinfo"]["email"](user_info)

        user_dto = self.user_repo.get_user_by_email(email)
        if not user_dto:
            # Создаем нового пользователя через AuthService
            username = email.split("@")[0]
            password = secrets.token_urlsafe(16)  # Генерируем случайный пароль
            result = self.auth_service.register_user(username, email, password)

            if "error" in result:
                raise ValueError(result["error"])

            user_dto = self.user_repo.get_user_by_email(email)

            # Отправляем приветственное письмо
            self.auth_service.email_service.send_welcome_email(user_dto)

        return user_dto

    def _get_access_token(self, provider_data: dict, code: str) -> str:
        """Получает токен доступа от провайдера."""
        try:
            response = requests.post(
                provider_data["token_url"],
                data={
                    "client_id": provider_data["client_id"],
                    "client_secret": provider_data["client_secret"],
                    "code": code,
                    "grant_type": "authorization_code",
                    "redirect_uri": url_for(
                        "oauth2_callback",
                        provider=provider_data["name"],
                        _external=True,
                    ),
                },
                headers={"Accept": "application/json"},
            )

            response.raise_for_status()
            return response.json().get("access_token")
        except SSLError:
            raise ValueError(
                "SSL certificate verification failed. Please check your system's date and time settings."
            )
        except Exception as e:
            raise ValueError(f"Failed to obtain access token: {str(e)}")

    def _get_user_info(self, provider_data: dict, token: str) -> dict:
        """Получает информацию о пользователе от провайдера."""
        try:
            response = requests.get(
                provider_data["userinfo"]["url"],
                headers={
                    "Authorization": "Bearer " + token,
                    "Accept": "application/json",
                },
            )

            response.raise_for_status()
            return response.json()
        except SSLError:
            raise ValueError(
                "SSL certificate verification failed while fetching user information."
            )
        except Exception as e:
            raise ValueError(f"Failed to fetch user information: {str(e)}")
