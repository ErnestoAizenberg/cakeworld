class ExchangeService:
    def __init__(self, currency_repository: "CurrencyRepository"):
        self.currency_repository = currency_repository

    def exchange_stones_for_gems(self, user_id: int) -> bool:
        """Обменивает 160 камней на 1 гем."""
        currency = self.currency_repository.get_currency_by_user_id(user_id)
        if currency and currency.stones >= 160:
            currency.stones -= 160
            currency.gems += 1
            self.currency_repository.save_currency(currency)
            logger.info(f"Exchanged stones for gems for user {user_id}.")
            return True
        logger.warning(f"User {user_id} has not enough stones to exchange.")
        return False
