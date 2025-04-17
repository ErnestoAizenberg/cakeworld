from typing import Any, Dict, List, Optional, Type, TypeVar

from sqlalchemy.exc import IntegrityError, NoResultFound, SQLAlchemyError
from sqlalchemy.orm import Session

T = TypeVar("T")  # Type of the model
DTO = TypeVar("DTO")  # Type of the DTO


class BaseRepository:
    def __init__(self, model: Type[T], dto_class: Type[DTO], db_session: Session):
        self.model = model
        self.dto_class = dto_class
        self.db_session = db_session

    def _to_dto(self, instance: T) -> DTO:
        """Converts model to DTO. Must be overridden in subclasses."""
        raise NotImplementedError("Method _to_dto must be overridden in a subclass")

    def _from_dto(self, dto: DTO) -> T:
        """Converts DTO to model. Must be overridden in subclasses."""
        raise NotImplementedError("Method _from_dto must be overridden in a subclass")

    def save(self, dto: DTO) -> DTO:
        instance = self._from_dto(dto)
        try:
            self.db_session.flush()  # Выгрузка текущих изменений
            self.db_session.merge(instance)
            self.db_session.commit()
            return self._to_dto(instance)
        except IntegrityError as e:
            self.db_session.rollback()
            raise ValueError(
                f"Integrity error occurred while saving. Details: {str(e)}"
            )
        except SQLAlchemyError as e:
            self.db_session.rollback()
            raise RuntimeError(
                f"Database error occurred while saving. Details: {str(e)}"
            )

    def get(self, id: int) -> Optional[DTO]:
        try:
            instance = self.db_session.query(self.model).get(id)
            if instance:
                return self._to_dto(instance)
            return None
        except NoResultFound:
            return None
        except SQLAlchemyError as e:
            raise RuntimeError(
                f"Database error occurred while retrieving data. Details: {str(e)}"
            )

    def get_all(self, **filters: Dict[str, Any]) -> List[DTO]:
        try:
            query = self.db_session.query(self.model)
            for key, value in filters.items():
                query = query.filter(getattr(self.model, key) == value)
            instances = query.all()
            return [self._to_dto(instance) for instance in instances]
        except SQLAlchemyError as e:
            raise RuntimeError(
                f"Database error occurred while retrieving all records. Details: {str(e)}"
            )

    def update(self, dto: DTO) -> DTO:
        try:
            existing_instance = self.db_session.query(self.model).get(dto.id)
            if not existing_instance:
                raise ValueError("Object with the specified identifier was not found")

            # Update attributes of existing object
            for key, value in dto.__dict__.items():
                if key != "id":  # Ensure we don't change the identifier
                    setattr(existing_instance, key, value)

            self.db_session.commit()
            return self._to_dto(existing_instance)

        except IntegrityError as e:
            self.db_session.rollback()
            raise ValueError(
                f"Integrity error occurred while updating. Details: {str(e)}"
            )
        except SQLAlchemyError as e:
            self.db_session.rollback()
            raise RuntimeError(
                f"Database error occurred while updating. Details: {str(e)}"
            )

    def delete(self, dto: DTO) -> bool:
        instance = self._from_dto(dto)
        try:
            self.db_session.delete(instance)
            self.db_session.commit()
            return True
        except ValueError as e:
            raise ValueError("Invalid object or identifier provided")
        except IntegrityError as e:
            self.db_session.rollback()
            raise ValueError(
                f"Integrity error occurred while deleting. Details: {str(e)}"
            )
        except SQLAlchemyError as e:
            self.db_session.rollback()
            raise RuntimeError(
                f"Database error occurred while deleting. Details: {str(e)}"
            )
