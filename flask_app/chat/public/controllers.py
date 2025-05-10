from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Optional


class ValidationError(Exception):
    pass


@dataclass
class ChatResponse:
    status: str
    message: str
    data: Optional[Dict[str, Any]] = None


class ChatController:
    def __init__(self, user_service, chat_service, message_service):
        self.user_service = user_service
        self.chat_service = chat_service
        self.message_service = message_service

    def create_chat(self, form_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Создает новый чат
        Args:
            form_data: {
                'title': str,
                'url_name': str,
                'is_private': bool,
                'description': str,
                'creator_id': int
            }
        Returns:
            {
                'status': 'success'|'error',
                'message': str,
                'chat': Optional[ChatDTO]
            }
        """
        try:
            chat_dto = self.chat_service.create_chat(
                title=form_data["title"],
                url_name=form_data["url_name"],
                is_private=form_data.get("is_private", False),
                description=form_data.get("description", ""),
            )

            # Добавляем создателя в чат
            self.chat_service.add_user_to_chat(
                user_id=form_data["creator_id"], chat_id=chat_dto.id
            )

            return {
                "status": "success",
                "message": "Чат успешно создан",
                "chat": chat_dto.dict(),
            }
        except ValidationError as e:
            return {
                "status": "error",
                "message": f"Ошибка валидации: {str(e)}",
                "chat": None,
            }
        except Exception:
            raise
            return {
                "status": "error",
                "message": "Ошибка при создании чата",
                "chat": None,
            }

    def join_to_chat(self, user_id: int, url_name: str) -> Dict[str, Any]:
        """
        Присоединяет пользователя к чату
        Args:
            user_id: ID пользователя
            url_name: URL идентификатор чата
        Returns:
            ChatResponse
        """
        try:
            chat = self.chat_service.get_chat_by_url(url_name)
            if not chat:
                return ChatResponse(status="error", message="Чат не найден").dict()

            if self.chat_service.is_user_in_chat(user_id, chat.id):
                return ChatResponse(
                    status="info", message="Вы уже состоите в этом чате"
                ).dict()

            if chat.is_private:
                return ChatResponse(
                    status="error",
                    message="Этот чат приватный, подайте заявку на вступление",
                ).dict()

            chat_user = self.chat_service.add_user_to_chat(user_id, chat.id)
            return ChatResponse(
                status="success",
                message="Вы успешно присоединились к чату",
                data={"chat_user": chat_user.dict()},
            ).dict()
        except Exception as e:
            return ChatResponse(
                status="error", message=f"Ошибка при присоединении к чату: {str(e)}"
            ).dict()

    def send_join_request(self, user_id: int, url_name: str) -> Dict[str, Any]:
        """
        Отправляет запрос на вступление в приватный чат
        Args:
            user_id: ID пользователя
            url_name: URL идентификатор чата
        Returns:
            ChatResponse
        """
        try:
            chat = self.chat_service.get_chat_by_url(url_name)
            if not chat:
                return ChatResponse(status="error", message="Чат не найден").dict()

            if not chat.is_private:
                return ChatResponse(
                    status="error",
                    message="Этот чат публичный, вы можете присоединиться напрямую",
                ).dict()

            if self.chat_service.is_user_in_chat(user_id, chat.id):
                return ChatResponse(
                    status="info", message="Вы уже состоите в этом чате"
                ).dict()

            # Создаем сообщение-запрос
            message = self.message_service.create_message(
                user_id=user_id,
                chat_id=chat.id,
                text=f"Запрос на вступление в чат от пользователя {user_id}",
                is_join_request=True,
            )

            return ChatResponse(
                status="success",
                message="Ваш запрос был отправлен",
                data={"message_id": message.id},
            ).dict()
        except Exception as e:
            return ChatResponse(
                status="error", message=f"Ошибка при отправке запроса: {str(e)}"
            ).dict()

    def handle_join_request(
        self, message_id: int, action: str, moderator_id: int
    ) -> Dict[str, Any]:
        """
        Обрабатывает запрос на вступление в чат
        Args:
            message_id: ID сообщения-запроса
            action: 'accept'|'reject'
            moderator_id: ID модератора, обрабатывающего запрос
        Returns:
            ChatResponse
        """
        try:
            if action == "accept":
                result = self.chat_service.accept_join_request(message_id)
                return ChatResponse(
                    status="success", message=result, data={"action": "accepted"}
                ).dict()
            elif action == "reject":
                result = self.chat_service.reject_join_request(message_id)
                return ChatResponse(
                    status="success", message=result, data={"action": "rejected"}
                ).dict()
            else:
                return ChatResponse(
                    status="error", message="Неизвестное действие"
                ).dict()
        except Exception as e:
            return ChatResponse(
                status="error", message=f"Ошибка при обработке запроса: {str(e)}"
            ).dict()

    def get_chat_info(self, url_name: int, user_id: int) -> Dict[str, Any]:
        """
        Получает информацию о чате и статусе пользователя в нем
        Args:
            url_name: chat url name
            user_id: user id
        Returns:
            ChatResponse
        """
        try:
            chat = self.chat_service.get_chat_by_url(url_name)
            if not chat:
                return ChatResponse(status="error", message="Чат не найден").dict()

            is_member = self.chat_service.is_user_in_chat(user_id, chat.id)
            users = self.chat_service.get_chat_users(chat.id)

            return ChatResponse(
                status="success",
                message="Информация о чате",
                data={
                    "chat": chat.dict(),
                    "is_member": is_member,
                    "members_count": len(users),
                    "is_private": chat.is_private,
                },
            ).dict()
        except Exception as e:
            return ChatResponse(
                status="error",
                message=f"Ошибка при получении информации о чате: {str(e)}",
            ).dict()

    def list_user_chats(self, user_id: int) -> Dict[str, Any]:
        """
        Получает список чатов пользователя
        Args:
            user_id: ID пользователя
        Returns:
            ChatResponse
        """
        try:
            chats = self.chat_service.get_user_chats(user_id)
            return ChatResponse(
                status="success",
                message="Список чатов пользователя",
                data={"chats": [chat.dict() for chat in chats]},
            ).dict()
        except Exception as e:
            return ChatResponse(
                status="error", message=f"Ошибка при получении списка чатов: {str(e)}"
            ).dict()

    def mute_user_in_chat(
        self, chat_id: int, user_id: int, moderator_id: int, until: datetime
    ) -> Dict[str, Any]:
        """
        Отключает звук у пользователя в чате
        Args:
            chat_id: ID чата
            user_id: ID пользователя
            moderator_id: ID модератора
            until: дата до которой действует mute
        Returns:
            ChatResponse
        """
        try:
            # Проверка прав модератора
            if not self._check_moderator_rights(moderator_id, chat_id):
                return ChatResponse(status="error", message="Недостаточно прав").dict()

            # Обновляем данные пользователя в чате
            chat_user = self.chat_service.add_user_to_chat(
                user_id=user_id, chat_id=chat_id, muted_until=until
            )

            return ChatResponse(
                status="success",
                message=f"Пользователь {user_id} отключен до {until}",
                data={"chat_user": chat_user.dict()},
            ).dict()
        except Exception as e:
            return ChatResponse(
                status="error", message=f"Ошибка при отключении пользователя: {str(e)}"
            ).dict()

    def _check_moderator_rights(self, user_id: int, chat_id: int) -> bool:
        """
        Проверяет, имеет ли пользователь права модератора в чате
        """
        # Здесь должна быть логика проверки прав
        # Например, проверка роли пользователя в чате
        return True
