import csv
from typing import List
import pandas as pd

from models import Sale, Sandal, Client


class SaleRepository:
    """
    Repositório de vendas que interage com um arquivo CSV para armazenar,
    recuperar, atualizar e excluir informações de vendas.

    Attributes:
        file_path (str): Caminho para o arquivo CSV onde os dados das vendas são armazenados.
        client_repository (ClientRepository): Repositório de clientes para buscar dados dos clientes.
        sandal_repository (SandalRepository): Repositório de sandálias para buscar dados das sandálias.
    """

    def __init__(self, file_path: str, sandal_repository, client_repository):
        """
        Args:
            file_path (str): Caminho para o arquivo CSV onde os dados das vendas serão lidos e escritos.
            sandal_repository (SandalRepository): Repositório de sandálias para realizar operações de pesquisa.
            client_repository (ClientRepository): Repositório de clientes para realizar operações de pesquisa.
        """
        self.client_repository = client_repository
        self.sandal_repository = sandal_repository
        self.file_path = file_path
        self._initialize_csv()  # Garantir que o arquivo CSV tenha cabeçalhos

    def _initialize_csv(self):
        """
        Inicializa o arquivo CSV com cabeçalhos, caso esteja vazio.

        Este método cria o arquivo CSV com os cabeçalhos necessários para armazenar informações de vendas
        caso o arquivo não exista.
        """
        try:
            with open(self.file_path, mode="x", newline="") as file:
                writer = csv.DictWriter(
                    file, fieldnames=["id", "client", "valor_total", "produtos"]
                )
                writer.writeheader()
        except FileExistsError:
            pass  # O arquivo já existe, então não precisamos fazer nada

    def create(self, sale: Sale) -> Sale:
        """
        Cria uma nova venda e a persiste no arquivo CSV.

        Args:
            sale (Sale): Objeto `Sale` com os dados da venda a ser criada.

        Returns:
            Sale: A venda criada com um ID atribuído.
        """
        sale.id = self._get_next_id()
        produtos_dict = self._produto_dict(sale.produtos)
        sale_dict = {
            "id": sale.id,
            "client": sale.client.id,
            "valor_total": sale.valor_total,
            "produtos": produtos_dict,
        }
        with open(self.file_path, mode="a", newline="") as file:
            writer = csv.DictWriter(
                file, fieldnames=["id", "client", "valor_total", "produtos"]
            )
            writer.writerow(sale_dict)
        return sale

    def search_por_id(self, sale_id: int) -> Sale | None:
        """
        Busca uma venda pelo ID.

        Args:
            sale_id (int): O ID da venda a ser buscada.

        Returns:
            Sale | None: A venda encontrada, ou `None` se não for encontrada.
        """
        with open(self.file_path, mode="r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if int(row["id"]) == sale_id:
                    produtos = self._search_produtos(
                        list(map(int, row["produtos"].split(",")))
                    )
                    client = self._bucar_client(int(row["client"]))
                    return Sale(
                        id=row["id"],
                        client=client,
                        valor_total=row["valor_total"],
                        produtos=produtos,
                    )
        return None

    def update(self, sale: Sale) -> Sale:
        """
        Atualiza os dados de uma venda no arquivo CSV.

        Args:
            sale (Sale): Objeto `Sale` contendo os dados atualizados da venda.

        Returns:
            Sale: A venda atualizada.

        Raises:
            ValueError: Se a venda não for encontrada.
        """
        sales = []
        updated: bool = False
        with open(self.file_path, mode="r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if int(row["id"]) == sale.id:
                    produtos_dict = self._produto_dict(sale.produtos)
                    sale_dict = {
                        "id": sale.id,
                        "client": sale.client.id,
                        "valor_total": sale.valor_total,
                        "produtos": produtos_dict,
                    }
                    sales.append(sale_dict)
                    updated = True
                else:
                    sales.append(row)

        with open(self.file_path, mode="w", newline="") as file:
            writer = csv.DictWriter(
                file, fieldnames=["id", "client", "valor_total", "produtos"]
            )
            writer.writeheader()
            writer.writerows(sales)

        if not updated:
            raise ValueError("User not found")
        return sale

    def delete(self, sale_id: int) -> bool:
        """
        Exclui uma venda pelo ID.

        Args:
            sale_id (int): O ID da venda a ser excluída.

        Returns:
            bool: `True` se a venda foi excluída com sucesso, `False` caso contrário.
        """
        sales: List[dict] = []
        deleted: bool = False
        with open(self.file_path, mode="r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if int(row["id"]) == sale_id:
                    deleted = True
                else:
                    sales.append(row)

        with open(self.file_path, mode="w", newline="") as file:
            writer = csv.DictWriter(
                file, fieldnames=["id", "client", "valor_total", "produtos"]
            )
            writer.writeheader()
            writer.writerows(sales)

        return deleted

    def list(self) -> List[Sale]:
        """
        Lista todas as vendas armazenadas no arquivo CSV.

        Returns:
            List[Sale]: Lista de objetos `Sale` com todas as vendas encontradas.
        """
        try:
            sales: List[Sale] = []
            with open(self.file_path, mode="r", newline="") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    produtos = self._search_produtos(
                        list(map(int, row["produtos"].split(",")))
                    )
                    client = self._bucar_client(int(row["client"]))
                    sales.append(
                        Sale(
                            id=row["id"],
                            client=client,
                            valor_total=row["valor_total"],
                            produtos=produtos,
                        )
                    )
            return sales
        except FileNotFoundError:
            pass

    def count(self):
        """
        Conta o número de vendas armazenadas no arquivo CSV.

        Returns:
            int: O número total de vendas registradas no arquivo CSV.
        """
        df = pd.read_csv(self.file_path)
        return df.shape[0]

    def _search_produtos(self, produtos: [int]) -> List[Sandal] | None:
        """
        Busca as sandálias baseadas nos IDs fornecidos.

        Args:
            produtos (List[int]): Lista de IDs das sandálias a serem buscadas.

        Returns:
            List[Sandal] | None: Lista de objetos `Sandal` encontrados, ou `None` se não encontrados.
        """
        produtos_list = []
        for produto in produtos:
            produtos_list.append(self.sandal_repository.search_por_id(produto))
        return produtos_list

    def _produto_dict(self, produtos: List[Sandal]) -> List[int] | None:
        """
        Converte uma lista de objetos `Sandal` para uma lista de IDs de sandálias.

        Args:
            produtos (List[Sandal]): Lista de objetos `Sandal`.

        Returns:
            List[int] | None: Lista de IDs das sandálias.
        """
        produto_dic: List[int] = []
        for produto in produtos:
            produto_dic.append(produto.id)
        return produto_dic

    def _bucar_client(self, client_id: int) -> Client | None:
        """
        Busca um cliente pelo ID.

        Args:
            client_id (int): O ID do cliente a ser buscado.

        Returns:
            Client | None: O cliente encontrado, ou `None` se não encontrado.
        """
        return self.client_repository.search_por_id(client_id)

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
