from models import Sandal
from repositories import SandalRepository


class SandalService:
    """
    Serviço que gerencia operações relacionadas a sandálias, incluindo a criação, pesquisa,
    listagem, atualização e exclusão de sandálias.

    Attributes:
        repository (SandalRepository): O repositório responsável pela persistência de dados das sandálias.
    """

    def __init__(self, repository: SandalRepository):
        """
        Inicializa o serviço de sandálias com o repositório de sandálias.

        Args:
            repository (SandalRepository): O repositório onde as sandálias são armazenadas.
        """
        self.repository = repository

    def create(self, sandal: Sandal) -> Sandal:
        """
        Cria uma nova sandália no repositório.

        Args:
            sandal (Sandal): A sandália a ser criada.

        Returns:
            Sandal: A sandália criada, incluindo seu ID atribuído.
        """
        return self.repository.create(sandal)

    def search_sandal(self, sandal_id: int) -> Sandal | None:
        """
        Busca uma sandália pelo seu ID.

        Args:
            sandal_id (int): O ID da sandália a ser buscada.

        Returns:
            Sandal | None: A sandália correspondente ao ID fornecido, ou None se não encontrada.
        """
        return self.repository.get_by_id(sandal_id)

    def list(self) -> list[Sandal]:
        """
        Lista todas as sandálias.

        Returns:
            list[Sandal]: Uma lista de todas as sandálias no repositório.
        """
        return self.repository.list()

    def update(self, sandal_id: int, sandal: Sandal) -> Sandal:
        """
        Atualiza os dados de uma sandália existente.

        Args:
            sandal_id (int): O ID da sandália a ser atualizada.
            sandal (Sandal): Os novos dados da sandália.

        Returns:
            Sandal: A sandália atualizada.

        Raises:
            ValueError: Se a sandália não for encontrada.
        """
        return self.repository.update(sandal)

    def delete(self, sandal_id: int) -> bool:
        """
        Exclui uma sandália pelo seu ID.

        Args:
            sandal_id (int): O ID da sandália a ser excluída.

        Returns:
            bool: True se a sandália foi excluída com sucesso, False caso contrário.
        """
        return self.repository.delete(sandal_id)
