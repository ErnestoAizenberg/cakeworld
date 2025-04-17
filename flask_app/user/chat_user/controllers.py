from flask import flash, jsonify, redirect, session


class UserChatController:
    def __init__(self, user_service, chat_service):
        self.user_service = user_service
        self.chat_service = chat_service

    def edit_account(self, new_username):
        user_id = session.get("user_id")
        if not user_id:
            return "User not logged in", 401

        user = self.user_service.get_user(user_id)
        if user is None:
            return "User not found", 404

        try:
            self.user_service.update_username(user.id, new_username)
            return "Username updated", 200
        except ValueError:
            return "Пользователь с таким ником уже существует :(", 400

    def get_profile(self, profile_url):
        owner_id = int(profile_url.split(".")[-1])
        owner = self.user_service.get_user(owner_id)

        if owner is None:
            return None, 404  # User not found

        return owner, 200

    def update_avatar(self, owner, file):
        owner.set_avatar(file)
        return owner.get_avatar_path()

    def list_users(self):
        return self.user_service.get_all_users()

    def api_users(self):
        users = self.list_users()
        return [
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "avatar_path": user.get_avatar_path(),
            }
            for user in users
        ]
