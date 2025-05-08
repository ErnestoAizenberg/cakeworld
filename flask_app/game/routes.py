
from flask import g, jsonify, render_template, request

from .currency.dtos import CurrencyDTO


# Mock данные
class DataReciver:
    def __init__(self, currency_service, banner_service, inventory_service):
        self.currency_service = currency_service
        self.banner_service = banner_service
        self.inventory_service = inventory_service

    def get_all(self, user_id):
        if user_id:
            user_currency = self.currency_service.get_currency(user_id)
        else:
            user_currency = CurrencyDTO()
        data = {
            "resources": user_currency,
            "banners": self.banner_service.get_all_banners(),
            "inventory": self.inventory_service.get_inventory_by_user_id(user_id),
            "daily_quests": [
                {
                    "title": "Ежедневная задача 1",
                    "progress": 5,
                    "goal": 10,
                    "reward": {"type": "gem", "amount": 10},
                },
                {
                    "title": "Ежедневная задача 2",
                    "progress": 3,
                    "goal": 8,
                    "reward": {"type": "stone", "amount": 5},
                },
                # Добавьте другие ежедневные квесты при необходимости
            ],
            "weekly_quests": [
                {
                    "title": "Недельная задача 1",
                    "progress": 1,
                    "goal": 1,
                    "reward": {"type": "gem", "amount": 20},
                }
                # Добавьте другие еженедельные квесты при необходимости
            ],
            "achievements": [
                {
                    "title": "Достижение 1",
                    "description": "Описание достижения 1.",
                    "progress": 50,
                    "goal": 100,
                },
                {
                    "title": "Достижение 2",
                    "description": "Описание достижения 2.",
                    "progress": 10,
                    "goal": 20,
                },
                # Добавьте другие достижения при необходимости
            ],
        }
        return data


import time



def init_game(app, data_reciver, prayer_service, inventory_service):
    @app.route("/game")
    def game_index():
        return render_template("game/game.html")

    @app.route("/game/data", methods=["GET"])
    def get_mock_game_data():
        if g.current_user:
            user_id = g.current_user.id
        else:
            user_id = 0
        mock_data = data_reciver.get_all(user_id)
        print("[DEBUG] game data: ", mock_data)
        return jsonify(mock_data)

    @app.route("/game/make_prayer", methods=["POST"])
    def make_prayer():
        data = request.get_json()
        banner_id = data.get("id")
        user = g.current_user

        # Здесь начинаем выполнение молитвы с таймаутом
        start_time = time.time()
        timeout = 1  # 1 секунда
        success = True
        while True:
            try:
                # Попробуем выполнить молитву
                result = prayer_service.perform_prayer(user.id, banner_id)
                if result:
                    inventory_service.add_or_update_item(
                        user_id=user.id,
                        store_item=result,
                        quantity=1,  # default is 1
                    )
                result_image = (
                    result.image_path
                    if result
                    else "/static/images/game/errors/link_to_fail_image.png"
                )
                break  # Успех, выходим из цикла
            except Exception as e:
                print(f"Error while making prayer: {str(e)}")
                result_image = "/static/images/game/error_500.png"
                break  # Выходим из цикла в случае ошибки

            # Проверка на таймаут
            if time.time() - start_time > timeout:
                result_image = "/static/images/game/errors/link_to_timeout_image.png"
                success = False
                break  # Выходим из цикла по истечению времени

        return jsonify({"success": success, "image": result_image})
