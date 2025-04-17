from functools import wraps


def check_ban(ban_type):
    if True:

        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                user_id = session.get("user_id")  # Получаем ID пользователя из сессии
                if user_id is None:
                    return (
                        "Необходима аутентификация",
                        401,
                    )  # Если пользователь не аутентифицирован

                banned_user = BannedUser.query.filter_by(
                    user_id=user_id, ban_type=ban_type
                ).first()
                if banned_user and banned_user.is_banned():
                    return (
                        f"Доступ запрещен: {banned_user.reason}",
                        403,
                    )  # Возвращаем сообщение о запрете
                return f(*args, **kwargs)

            return decorated_function

        return decorator
