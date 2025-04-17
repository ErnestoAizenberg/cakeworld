import logging
import random
from typing import Optional

from flask import current_app

from flask_app.extensions import db
from flask_app.game.currency.repositories import CurrencyRepository
from flask_app.game.item.code.dtos import ItemCodeDTO

from .dtos import PrayerResultDTO

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PrayerService:
    MAX_PRAYERS_PER_DAY = 70

    def __init__(
        self,
        prayer_repository: "PrayerRepository",
        item_service: "ItemService",
        currency_repository: CurrencyRepository,
    ):
        self.prayer_repository = prayer_repository
        self.item_service = item_service
        self.currency_repository = currency_repository

    def perform_prayer(self, user_id: int, banner_id: int) -> Optional[ItemCodeDTO]:
        """Выполняет молитву от имени пользователя."""

        # Начинаем сессию базы данных в контексте приложения
        with current_app.app_context():
            try:
                prayer_count = self.prayer_repository.count_today_prayers(user_id)
                if prayer_count >= self.MAX_PRAYERS_PER_DAY:
                    raise ValueError("Достигнут дневной лимит молитв.")

                currency = self.currency_repository.get_currency_by_user_id(user_id)
                if not currency or currency.gems < 1:
                    raise ValueError("Недостаточно гемов для молитвы.")

                # Уменьшаем количество гемов на 1
                currency.gems -= 1
                self.currency_repository.update(currency)

                item = None
                if random.random() < 1:  # 10% шанс
                    item = self.get_random_item()
                    if item:
                        prayer_result = PrayerResultDTO(
                            user_id=user_id,
                            banner_id=banner_id,
                            item_id=item.id,
                        )
                        self.prayer_repository.save(
                            prayer_result,
                        )

                # Если не получили предмет, все равно сохраняем результат молитвы
                if item is None:
                    prayer_result = PrayerResultDTO(
                        user_id=user_id, banner_id=banner_id
                    )
                    self.prayer_repository.save(prayer_result)

                db.session.commit()  # Подтверждаем изменения в БД
                logger.info(
                    f"Prayer executed successfully for user {user_id}. Item: {item if item else None}."
                )
                return item

            except ValueError as ve:
                db.session.rollback()  # Откатываем изменения в случае ошибки
                logger.warning(
                    f"ValueError while performing prayer for user {user_id}: {str(ve)}"
                )
                raise

            except ConnectionError as ce:
                db.session.rollback()
                logger.error(
                    f"Database connection error while performing prayer for user {user_id}: {str(ce)}"
                )
                raise RuntimeError("Ошибка подключения к базе данных.") from ce

            except Exception as e:
                db.session.rollback()  # Откатываем изменения в случае неизвестной ошибки
                logger.error("Unexpected error performing prayer", exc_info=e)
                raise RuntimeError("Произошла непредвиденная ошибка.") from e

    def get_random_item(self) -> Optional[ItemCodeDTO]:
        """Получает случайный предмет."""
        with current_app.app_context():
            try:
                items = self.item_service.get_all_items()
                if not items:
                    logger.warning("No items available to select a random item.")
                    return None
                random_item = random.choice(items)
                return random_item

            except Exception as e:
                logger.error("Error fetching random item", exc_info=e)
                raise RuntimeError("Ошибка получения случайного предмета.") from e
