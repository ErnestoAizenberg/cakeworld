from flask import jsonify, request

from flask_app import app
from flask_app.services import CurrencyService, ExchangeService

from .repositories import CurrencyRepository

# Создаем экземпляры репозиториев и сервисов
currency_repository = CurrencyRepository()
currency_service = CurrencyService(currency_repository)
exchange_service = ExchangeService(currency_repository)


@app.route("/currency/<int:user_id>", methods=["GET"])
def get_currency(user_id: int):
    """Получить валюту пользователя."""
    currency = currency_service.get_currency(user_id)
    if currency:
        return (
            jsonify(
                {
                    "user_id": currency.user_id,
                    "coins": currency.coins,
                    "stones": currency.stones,
                    "gems": currency.gems,
                }
            ),
            200,
        )
    return jsonify({"error": "Currency not found"}), 404


@app.route("/currency/<int:user_id>/add_resource", methods=["POST"])
def add_resource(user_id: int):
    """Добавить ресурсы пользователю."""
    data = request.get_json()

    if not data or "resource" not in data or "amount" not in data:
        return jsonify({"error": "Missing resource or amount"}), 400

    resource = data["resource"]
    amount = data["amount"]

    # Проверка на корректность amount
    if not isinstance(amount, int) or amount < 0:
        return jsonify({"error": "Invalid amount. Must be a positive integer."}), 400

    try:
        # Добавляем соответствующие ресурсы
        if resource == "coins":
            currency = currency_service.add_coins(user_id, amount)
        elif resource == "stones":
            currency = currency_service.add_stones(user_id, amount)
        elif resource == "gems":
            currency = currency_service.add_gems(user_id, amount)
        else:
            return jsonify({"error": "Invalid resource type"}), 400

        return (
            jsonify(
                {
                    "user_id": currency.user_id,
                    "coins": currency.coins,
                    "stones": currency.stones,
                    "gems": currency.gems,
                }
            ),
            200,
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Общий ответ для внутренних ошибок


@app.route("/currency/<int:user_id>/exchange_stones_for_gems", methods=["POST"])
def exchange_stones_for_gems(user_id: int):
    """Обменять камни на гемы."""
    success = exchange_service.exchange_stones_for_gems(user_id)
    if success:
        return jsonify({"message": "Exchange successful."}), 200
    return jsonify({"error": "Not enough stones to exchange."}), 400
