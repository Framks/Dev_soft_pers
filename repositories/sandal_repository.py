import csv
from typing import Optional, List
from models import Sandal


class SandalRepository:
    """
    Repositório de sandálias que interage com um arquivo CSV para armazenar,
    recuperar, atualizar e excluir informações de sandálias.

    Attributes:
        file_path (str): Caminho para o arquivo CSV onde os dados das sandálias são armazenados.
    """

    def __init__(self, file_path: str):
        """
        Args:
            file_path (str): Caminho para o arquivo CSV onde os dados das sandálias serão lidos e escritos.
        """
        self.file_path = file_path
        self._initialize_csv()  # Garantir que o arquivo CSV tenha cabeçalhos

    def _initialize_csv(self):
        """
        Inicializa o arquivo CSV com cabeçalhos, caso esteja vazio.

        Este método cria o arquivo CSV com os cabeçalhos necessários para armazenar informações de sandálias
        caso o arquivo não exista.
        """
        try:
            with open(self.file_path, mode="x", newline="") as file:
                writer = csv.DictWriter(
                    file,
                    fieldnames=[
                        "id",
                        "codigo",
                        "nome",
                        "quantidade",
                        "valor",
                        "cor",
                        "tamanho",
                    ],
                )
                writer.writeheader()
        except FileExistsError:
            pass  # O arquivo já existe, então não precisamos fazer nada

    def create(self, sandal: Sandal) -> Sandal:
        """
        Cria uma nova sandália e a persiste no arquivo CSV.

        Args:
            sandal (Sandal): Objeto `Sandal` com os dados da sandália a ser criada.

        Returns:
            Sandal: A sandália criada com um ID atribuído.
        """
        sandal.id = self._get_next_id()
        with open(self.file_path, mode="a", newline="") as file:
            writer = csv.DictWriter(
                file,
                fieldnames=[
                    "id",
                    "codigo",
                    "nome",
                    "quantidade",
                    "valor",
                    "cor",
                    "tamanho",
                ],
            )
            writer.writerow(sandal.model_dump())
        return sandal

    def search_por_id(self, sandal_id: int) -> Optional[Sandal]:
        """
        Busca uma sandália pelo ID.

        Args:
            sandal_id (int): O ID da sandália a ser buscada.

        Returns:
            Optional[Sandal]: A sandália encontrada ou `None` se não for encontrada.
        """
        with open(self.file_path, mode="r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if int(row["id"]) == sandal_id:
                    return Sandal(**row)
        return None

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
        sandals = []
        updated = False
        with open(self.file_path, mode="r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if int(row["id"]) == sandal.id:
                    sandals.append(sandal.model_dump())
                    updated = True
                else:
                    sandals.append(row)

        with open(self.file_path, mode="w", newline="") as file:
            writer = csv.DictWriter(
                file,
                fieldnames=[
                    "id",
                    "codigo",
                    "nome",
                    "quantidade",
                    "valor",
                    "cor",
                    "tamanho",
                ],
            )
            writer.writeheader()
            writer.writerows(sandals)

        if not updated:
            raise ValueError("User not found")
        return sandal

    def delete(self, sandal_id: int) -> bool:
        """
        Exclui uma sandália pelo ID.

        Args:
            sandal_id (int): O ID da sandália a ser excluída.

        Returns:
            bool: `True` se a sandália foi excluída com sucesso, `False` caso contrário.
        """
        sandals = []
        deleted = False
        with open(self.file_path, mode="r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if int(row["id"]) == sandal_id:
                    deleted = True
                else:
                    sandals.append(row)

        with open(self.file_path, mode="w", newline="") as file:
            writer = csv.DictWriter(
                file,
                fieldnames=[
                    "id",
                    "codigo",
                    "nome",
                    "quantidade",
                    "valor",
                    "cor",
                    "tamanho",
                ],
            )
            writer.writeheader()
            writer.writerows(sandals)

        return deleted

    def list(self) -> List[Sandal]:
        """
        Lista todas as sandálias armazenadas no arquivo CSV.

        Returns:
            List[Sandal]: Lista de objetos `Sandal` com todas as sandálias encontradas.
        """
        try:
            sandals: List[Sandal] = []
            with open(self.file_path, mode="r", newline="") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    sandals.append(Sandal(**row))
            return sandals
        except FileNotFoundError:
            pass

    def _get_next_id(self) -> int:
        """
        Gera o próximo ID com base no maior ID existente no arquivo CSV.

        Returns:
            int: O próximo ID disponível.
        """
        max_id = 0
        with open(self.file_path, mode="r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                max_id = max(max_id, int(row["id"]))
        return max_id + 1
