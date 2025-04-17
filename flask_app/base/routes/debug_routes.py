import json

from flask import Flask, jsonify, redirect, request, session

from flask_app import app
from flask_app.services import CurrencyService


@app.route("/currency/debug", methods=["GET", "POST", "DELETE"])
def manage_currency():
    """Управление валютой пользователя."""
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({"error": "Пользователь не авторизован"}), 401

    if request.method == "GET":
        return get_balance(user_id)
    elif request.method == "POST":
        return add_currency(user_id, request.json)
    elif request.method == "DELETE":
        return deduct_currency(user_id, request.json)


def get_balance(user_id):
    """Возвращает баланс пользователя."""
    balance = CurrencyService.get_balance(user_id)
    return jsonify({"balance": balance})


def add_currency(user_id, data):
    """Добавляет валюту пользователю."""
    amount = data.get("amount", 0)
    if amount <= 0:
        return jsonify({"error": "Сумма должна быть положительной"}), 400

    CurrencyService.add_currency(user_id, amount)
    return jsonify({"message": f"Добавлено {amount} единиц валюты."})


def deduct_currency(user_id, data):
    """Списывает валюту с баланса пользователя."""
    amount = data.get("amount", 0)
    if amount <= 0:
        return jsonify({"error": "Сумма должна быть положительной"}), 400

    success = CurrencyService.deduct_currency(user_id, amount)
    if success:
        return jsonify({"message": f"Списано {amount} единиц валюты."})
    else:
        return jsonify({"error": "Недостаточно средств."}), 400


@app.route("/mock_messages/<int:amount>")
def create_mock_messages(amount):
    for i in range(amount):
        message = Message(
            text="mock_text" + " " + str(i), author="Aizeн", user_id=2, chat_id=1
        )
        db.session.add(message)
    db.session.commit()

    return redirect("/")
