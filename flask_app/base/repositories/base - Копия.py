from typing import Any, Dict, List, Optional, Type, TypeVar

from sqlalchemy.orm import Session

T = TypeVar("T")  # Тип модели
DTO = TypeVar("DTO")  # Тип DTO


class BaseRepository:
    def __init__(self, model: Type[T], dto_class: Type[DTO], db_session: Session):
        self.model = model
        self.dto_class = dto_class
        self.db_session = db_session

    def _to_dto(self, instance: T) -> DTO:
        """Преобразует модель в DTO. Должен быть переопределен в дочерних классах."""
        raise NotImplementedError(
            "Метод _to_dto должен быть переопределен в дочернем классе"
        )

    def _from_dto(self, dto: DTO) -> T:
        """Преобразует DTO в модель. Должен быть переопределен в дочерних классах."""
        raise NotImplementedError(
            "Метод _from_dto должен быть переопределен в дочернем классе"
        )

    def save(self, dto: DTO) -> DTO:
        instance = self._from_dto(dto)
        self.db_session.add(instance)
        self.db_session.commit()
        return self._to_dto(instance)

    def get(self, id: int) -> Optional[DTO]:
        instance = self.db_session.query(self.model).get(id)
        if instance:
            return self._to_dto(instance)
        return None

    def get_all(self, **filters: Dict[str, Any]) -> List[DTO]:
        query = self.db_session.query(self.model)
        for key, value in filters.items():
            query = query.filter(getattr(self.model, key) == value)
        instances = query.all()
        return [self._to_dto(instance) for instance in instances]

    def update(self, dto: DTO) -> DTO:
        instance = self._from_dto(dto)
        self.db_session.commit()
        return self._to_dto(instance)

    def update(self, dto: DTO) -> DTO:
        # Предполагаем, что идентификатор объекта содержится в самом DTO
        existing_instance = self.db_session.query(self.model).get(dto.id)
        if not existing_instance:
            raise ValueError("Объект с указанным идентификатором не найден")

        # Обновляем атрибуты существующего объекта
        for key, value in dto.__dict__.items():
            if key != "id":  # Вадно что не изменяем идентификатор
                setattr(existing_instance, key, value)

        self.db_session.commit()
        return self._to_dto(existing_instance)

    def delete(self, dto: DTO) -> bool:
        instance = self._from_dto(dto)
        self.db_session.delete(instance)
        self.db_session.commit()
        return True
