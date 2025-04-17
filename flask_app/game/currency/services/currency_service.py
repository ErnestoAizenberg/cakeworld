import logging
from typing import Optional

from flask_app.extensions import db

from ..models import Currency
from ..repositories import CurrencyRepository

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CurrencyService:
    def __init__(self, currency_repository: "CurrencyRepository"):
        self.currency_repository = currency_repository

    def get_currency(self, user_id: int) -> Optional[Currency]:
        """Возвращает валюту пользователя."""
        return self.currency_repository.get_currency_by_user_id(user_id)

    def _validate_amount(self, amount: int):
        if amount < 0:
            raise ValueError("Amount must be a positive number.")

    def add_coins(self, user_id: int, amount: int) -> Currency:
        """Добавляет монеты пользователю."""
        self._validate_amount(amount)

        try:
            currency = self.get_currency(user_id)
            if not currency:
                currency = self.currency_repository.create_currency(
                    user_id, coins=amount
                )
            else:
                currency.coins += amount
                self.currency_repository.save_currency(currency)
            logger.info(f"Added {amount} coins to user {user_id}.")
            return currency
        except Exception as e:
            db.session.rollback()
            logger.error(f"Failed to add coins to user {user_id}: {e}")
            raise

    def add_stones(self, user_id: int, amount: int) -> Currency:
        """Добавляет камни пользователю."""
        self._validate_amount(amount)

        try:
            currency = self.get_currency(user_id)
            if not currency:
                currency = self.currency_repository.create_currency(
                    user_id, stones=amount
                )
            else:
                currency.stones += amount
                self.currency_repository.save_currency(currency)
            logger.info(f"Added {amount} stones to user {user_id}.")
            return currency
        except Exception as e:
            db.session.rollback()
            logger.error(f"Failed to add stones to user {user_id}: {e}")
            raise

    def add_gems(self, user_id: int, amount: int) -> Currency:
        """Добавляет гемы пользователю."""
        self._validate_amount(amount)

        try:
            currency = self.get_currency(user_id)
            if not currency:
                currency = self.currency_repository.create_currency(
                    user_id, gems=amount
                )
            else:
                currency.gems += amount
                self.currency_repository.save_currency(currency)
            logger.info(f"Added {amount} gems to user {user_id}.")
            return currency
        except Exception as e:
            db.session.rollback()
            logger.error(f"Failed to add gems to user {user_id}: {e}")
            raise
