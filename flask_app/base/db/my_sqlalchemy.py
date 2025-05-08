from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError


class CustomSQLAlchemy(SQLAlchemy):
    def create_scoped_session(self, options=None):
        """Override the create_scoped_session to control session behavior."""
        session_options = options or {}
        session_options["autoflush"] = False  # Выключаем автоматический флипс
        return super().create_scoped_session(options=session_options)

    def add(self, obj):
        """Override the add method to include error handling."""
        session = self.session

        try:
            # Проверка, требуется ли добавление объекта
            if obj not in session:
                session.add(obj)  # Используем стандартный метод add

            # Выполняем флипс явно
            session.flush()  # Или session.commit(), если хотите зафиксировать сразу

        except OperationalError as e:
            session.rollback()
            raise RuntimeError(
                f"Database error occurred while adding. Details: {str(e)}"
            )

        except RuntimeError as e:
            session.rollback()
            raise RuntimeError(f"An unexpected runtime error occurred: {str(e)}")

        except Exception as e:
            session.rollback()
            raise RuntimeError(f"An unexpected error occurred: {str(e)}")

    def save(self, obj):
        """Save an object to the database with error handling."""
        session = self.session

        try:
            self.add(obj)  # Используем свой переопределенный метод add
            session.commit()  # Зафиксируем изменения после добавления

        except Exception as e:
            session.rollback()
            raise RuntimeError(f"An unexpected error occurred while saving: {str(e)}")
