import csv
from typing import List
import pandas as pd

from models import Client


class ClientRepository:
    """
    Repositório de clientes que interage com um arquivo CSV para armazenar,
    recuperar, atualizar e excluir informações de clientes.

    Attributes:
        file_path (str): Caminho para o arquivo CSV onde os dados dos clientes são armazenados.
        proximo_id (int): O próximo ID disponível para a criação de um cliente.
        data_base (List[dict]): A lista de clientes carregados do arquivo CSV.
    """

    def __init__(self, file_path: str):
        """
        Args:
            file_path (str): Caminho para o arquivo CSV onde os dados dos clientes serão lidos e escritos.
        """
        self.file_path = file_path
        self.proximo_id = 0
        self.data_base = self._initialize_csv()

    def _initialize_csv(self):
        """
        Inicializa a base de dados a partir do arquivo CSV, ou cria um novo arquivo se não existir.

        Retorna:
            List[dict]: Lista de clientes carregada do arquivo CSV.
        """
        try:
            df = pd.read_csv(self.file_path)
            self.proximo_id = int(df["id"].max() + 1)
            client_list = []
            for index, row in df.iterrows():
                client_list.append(
                    {
                        "id": row["id"],
                        "nome": row["nome"],
                        "celular": row["celular"],
                        "endereco": row["endereco"],
                    }
                )
            return client_list
        except FileExistsError:
            with open(self.file_path, mode="x", newline="") as file:
                writer = csv.DictWriter(
                    file, fieldnames=["id", "nome", "celular", "endereco"]
                )
                writer.writeheader()
            return []

    def create(self, client: Client) -> Client:
        """
        Cria um novo cliente e persiste no arquivo CSV.

        Args:
            client (Client): Objeto `Client` com os dados do cliente a ser criado.

        Returns:
            Client: O cliente criado com um ID atribuído.
        """
        client.id = self.proximo_id
        self.proximo_id += 1
        self.data_base.append(client.model_dump())
        with open(self.file_path, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(
                file, fieldnames=["id", "nome", "celular", "endereco"]
            )
            writer.writerow(client.model_dump())
        return client

    def search_por_id(self, client_id: int) -> Client | None:
        """
        Busca um cliente pelo ID.

        Args:
            client_id (int): O ID do cliente a ser buscado.

        Returns:
            Client | None: O cliente encontrado, ou `None` se não encontrado.
        """
        try:
            return Client.from_dict(self._find(client_id))
        except IndexError:
            return None

    def update(self, client: Client) -> Client:
        """
        Atualiza as informações de um cliente no arquivo CSV.

        Args:
            client (Client): Objeto `Client` contendo os dados atualizados do cliente.

        Returns:
            Client: O cliente atualizado.

        Raises:
            ValueError: Se o cliente não for encontrado.
        """
        updated = False
        client_achado = self._find(client.id)
        if client_achado:
            updated = True
            self.data_base.remove(client_achado)
            self.data_base.append(client.model_dump())
            with open(self.file_path, mode="w", newline="") as file:
                writer = csv.DictWriter(
                    file, fieldnames=["id", "nome", "celular", "endereco"]
                )
                writer.writeheader()
                writer.writerows(self.data_base)

        if not updated:
            raise ValueError("User not found")
        return client

    def delete(self, client_id: int) -> bool:
        """
        Exclui um cliente pelo ID do arquivo CSV.

        Args:
            client_id (int): O ID do cliente a ser excluído.

        Returns:
            bool: `True` se o cliente foi excluído com sucesso, `False` caso contrário.
        """
        client_achado = self._find(client_id)
        deleted = False
        if client_achado:
            deleted = True
            self.data_base.remove(client_achado)
            with open(self.file_path, mode="w", newline="") as file:
                writer = csv.DictWriter(
                    file, fieldnames=["id", "nome", "celular", "endereco"]
                )
                writer.writeheader()
                writer.writerows(self.data_base)

        return deleted

    def list(self) -> List[Client]:
        """
        Lista todos os clientes armazenados no arquivo CSV.

        Returns:
            List[Client]: Lista de objetos `Client` com todos os clientes encontrados.
        """
        try:
            return [Client.from_dict(data=row) for row in self.data_base]
        except FileNotFoundError:
            return []

    def _find(self, id: int):
        """
        Busca um cliente pelo ID dentro da base de dados carregada.

        Args:
            id (int): O ID do cliente a ser buscado.

        Returns:
            dict | None: O cliente encontrado ou `None` se não encontrado.
        """
        for client in self.data_base:
            if client["id"] == id:
                return client
        return None
