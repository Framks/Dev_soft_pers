from sqlmodel import Session, select

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

    def __init__(self, session: Session):
        """
        Args:
            file_path (str): Caminho para o arquivo CSV onde os dados das vendas serão lidos e escritos.
            sandal_repository (SandalRepository): Repositório de sandálias para realizar operações de pesquisa.
            client_repository (ClientRepository): Repositório de clientes para realizar operações de pesquisa.
        """
        self.session = session

    def create(self, sale: Sale) -> Sale:
        """
        Cria uma nova venda e a persiste no arquivo CSV.

        Args:
            sale (Sale): Objeto `Sale` com os dados da venda a ser criada.

        Returns:
            Sale: A venda criada com um ID atribuído.
        """
        self.session.add(sale)
        self.session.commit()
        self.session.refresh(sale)
        return sale

    def get_by_id(self, sale_id: int) -> Sale | None:
        """
        Busca uma venda pelo ID.

        Args:
            sale_id (int): O ID da venda a ser buscada.

        Returns:
            Sale | None: A venda encontrada, ou `None` se não for encontrada.
        """
        return self.session.get(Sale, sale_id)

    def update(self, sale: Sale) -> Sale | None:
        """
        Atualiza os dados de uma venda no arquivo CSV.

        Args:
            sale (Sale): Objeto `Sale` contendo os dados atualizados da venda.

        Returns:
            Sale: A venda atualizada.

        Raises:
            ValueError: Se a venda não for encontrada.
        """
        sale_before = self.get_by_id(sale.id)
        if not sale_before:
            return None
        for key, value in sale.model_dump().items():
            setattr(sale_before, key,value)
        self.session.commit()
        self.session.refresh(sale)
        return sale

    def delete(self, sale_id: int) -> bool:
        """
        Exclui uma venda pelo ID.

        Args:
            sale_id (int): O ID da venda a ser excluída.

        Returns:
            bool: `True` se a venda foi excluída com sucesso, `False` caso contrário.
        """
        sale = self.get_by_id(sale_id)
        if not sale:
            return False
        self.session.delete(sale)
        self.session.commit()
        return True

    def list(self):
        """
        Lista todas as vendas armazenadas no arquivo CSV.

        Returns:
            List[Sale]: Lista de objetos `Sale` com todas as vendas encontradas.
        """
        try:
            return self.session.exec(select(Sale)).all()
        except FileNotFoundError:
            pass