import logging
from typing import Any, Dict, List, Optional, Type, TypeVar

from sqlalchemy.exc import IntegrityError, NoResultFound, SQLAlchemyError
from sqlalchemy.orm import Session


# ANSI escape sequences for colored terminal output
class ConsoleColors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


# Set up logging
logging.basicConfig(level=logging.DEBUG, format="%(message)s")
logger = logging.getLogger(__name__)

T = TypeVar("T")  # Type of the model
DTO = TypeVar("DTO")  # Type of the DTO


class BaseRepository:
    def __init__(self, model: Type[T], dto_class: Type[DTO], db_session: Session):
        self.model = model
        self.dto_class = dto_class
        self.db_session = db_session
        logger.info(
            f"{ConsoleColors.OKGREEN}Initialized repository for model: {self.model.__name__}{ConsoleColors.ENDC}"
        )

    def _to_dto(self, instance: T) -> DTO:
        """Converts model to DTO. Must be overridden in subclasses."""
        raise NotImplementedError("Method _to_dto must be overridden in a subclass")

    def _from_dto(self, dto: DTO) -> T:
        """Converts DTO to model. Must be overridden in subclasses."""
        raise NotImplementedError("Method _from_dto must be overridden in a subclass")

    def save(self, dto: DTO) -> DTO:
        instance = self._from_dto(dto)
        self.db_session.add(instance)
        self.db_session.commit()
        return self._to_dto(instance)

    def get(self, id: int) -> Optional[DTO]:
        logger.debug(
            f"{ConsoleColors.OKBLUE}Attempting to retrieve object with id: {id}{ConsoleColors.ENDC}"
        )
        try:
            instance = self.db_session.query(self.model).get(id)
            if instance:
                logger.info(
                    f"{ConsoleColors.OKGREEN}Object retrieved: {self._to_dto(instance)}{ConsoleColors.ENDC}"
                )
                return self._to_dto(instance)
            logger.warning(
                f"{ConsoleColors.WARNING}No object found with id: {id}{ConsoleColors.ENDC}"
            )
            return None
        except NoResultFound:
            logger.warning(
                f"{ConsoleColors.WARNING}No result found for id: {id}{ConsoleColors.ENDC}"
            )
            return None
        except SQLAlchemyError as e:
            logger.error(
                f"{ConsoleColors.FAIL}Database error occurred while retrieving data. Details: {str(e)}{ConsoleColors.ENDC}"
            )
            raise RuntimeError(
                f"Database error occurred while retrieving data. Details: {str(e)}"
            )

    def get_all(self, **filters: Dict[str, Any]) -> List[DTO]:
        logger.debug(
            f"{ConsoleColors.OKBLUE}Retrieving all objects with filters: {filters}{ConsoleColors.ENDC}"
        )
        try:
            query = self.db_session.query(self.model)
            for key, value in filters.items():
                query = query.filter(getattr(self.model, key) == value)
            instances = query.all()
            logger.info(
                f"{ConsoleColors.OKGREEN}Retrieved {len(instances)} objects{ConsoleColors.ENDC}"
            )
            return [self._to_dto(instance) for instance in instances]
        except SQLAlchemyError as e:
            logger.error(
                f"{ConsoleColors.FAIL}Database error occurred while retrieving all records. Details: {str(e)}{ConsoleColors.ENDC}"
            )
            raise RuntimeError(
                f"Database error occurred while retrieving all records. Details: {str(e)}"
            )

    def update(self, dto: DTO) -> DTO:
        logger.debug(
            f"{ConsoleColors.OKBLUE}Attempting to update DTO: {dto}{ConsoleColors.ENDC}"
        )
        try:
            existing_instance = self.db_session.query(self.model).get(dto.id)
            if not existing_instance:
                logger.error(
                    f"{ConsoleColors.FAIL}Object with the specified identifier was not found: {dto.id}{ConsoleColors.ENDC}"
                )
                raise ValueError("Object with the specified identifier was not found")

            # Update attributes of existing object
            for key, value in dto.__dict__.items():
                if key != "id":  # Ensure we don't change the identifier
                    setattr(existing_instance, key, value)

            self.db_session.commit()
            logger.info(
                f"{ConsoleColors.OKGREEN}Successfully updated DTO: {self._to_dto(existing_instance)}{ConsoleColors.ENDC}"
            )
            return self._to_dto(existing_instance)

        except IntegrityError as e:
            self.db_session.rollback()
            logger.error(
                f"{ConsoleColors.FAIL}Integrity error occurred while updating. Details: {str(e)}{ConsoleColors.ENDC}"
            )
            raise ValueError(
                f"Integrity error occurred while updating. Details: {str(e)}"
            )
        except SQLAlchemyError as e:
            self.db_session.rollback()
            logger.error(
                f"{ConsoleColors.FAIL}Database error occurred while updating. Details: {str(e)}{ConsoleColors.ENDC}"
            )
            raise RuntimeError(
                f"Database error occurred while updating. Details: {str(e)}"
            )

    def delete(self, dto: DTO) -> bool:
        logger.debug(
            f"{ConsoleColors.OKBLUE}Attempting to delete DTO: {dto}{ConsoleColors.ENDC}"
        )
        instance = self._from_dto(dto)
        try:
            self.db_session.delete(instance)
            self.db_session.commit()
            logger.info(
                f"{ConsoleColors.OKGREEN}Successfully deleted DTO: {dto}{ConsoleColors.ENDC}"
            )
            return True
        except ValueError as e:
            logger.error(
                f"{ConsoleColors.FAIL}Invalid object or identifier provided: {dto}{ConsoleColors.ENDC}"
            )
            raise ValueError("Invalid object or identifier provided")
        except IntegrityError as e:
            self.db_session.rollback()
            logger.error(
                f"{ConsoleColors.FAIL}Integrity error occurred while deleting. Details: {str(e)}{ConsoleColors.ENDC}"
            )
            raise ValueError(
                f"Integrity error occurred while deleting. Details: {str(e)}"
            )
        except SQLAlchemyError as e:
            self.db_session.rollback()
            logger.error(
                f"{ConsoleColors.FAIL}Database error occurred while deleting. Details: {str(e)}{ConsoleColors.ENDC}"
            )
            raise RuntimeError(
                f"Database error occurred while deleting. Details: {str(e)}"
            )
