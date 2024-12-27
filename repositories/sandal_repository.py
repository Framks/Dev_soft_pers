import csv
from typing import Optional, List

from sqlmodel import Session, select

from exceptions import OperationalException, NotFoundException
from models import Sandal


class SandalRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, sandal: Sandal) -> Sandal:
        try:
            self.session.add(sandal)
            self.session.commit()
            self.session.refresh(sandal)
            return sandal
        except Exception as e:
            self.session.rollback()
            raise OperationalException(str(e))

    def get_by_id(self, sandal_id: int) -> Optional[Sandal]:
        """
        Busca uma sandália pelo ID.

        Args:
            sandal_id (int): O ID da sandália a ser buscada.

        Returns:
            Optional[Sandal]: A sandália encontrada ou `None` se não for encontrada.
        """
        try:
            return self.session.get(Sandal, sandal_id)
        except Exception as e:
            raise OperationalException(str(e))

    def update(self, sandal: Sandal) -> Sandal:
        """
        Atualiza os dados de uma sandália no arquivo CSV.

        Args:
            sandal (Sandal): Objeto `Sandal` contendo os dados atualizados da sandália.

        Returns:
            Sandal: A sandália atualizada.

        Raises:
            ValueError: Se a sandália não for encontrada.
        """
        try:
            before = self.get_by_id(sandal.id)
            for key, value in sandal.model_dump().items():
                setattr(before, key, value)
            self.session.commit()
            return before
        except Exception as e:
            self.session.rollback()
            raise NotFoundException(str(e))

    def delete(self, sandal_id: int) -> bool:
        """
        Exclui uma sandália pelo ID.

        Args:
            sandal_id (int): O ID da sandália a ser excluída.

        Returns:
            bool: `True` se a sandália foi excluída com sucesso, `False` caso contrário.
        """
        try:
            sandal = self.get_by_id(sandal_id)
            self.session.delete(sandal)
            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            raise NotFoundException(str(e))

    def list(self):
        """
        Lista todas as sandálias armazenadas no arquivo CSV.

        Returns:
            List[Sandal]: Lista de objetos `Sandal` com todas as sandálias encontradas.
        """
        try:
            return self.session.exec(select(Sandal)).all()
        except Exception as e:
            raise OperationalException(str(e))
