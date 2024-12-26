import zipfile
from fastapi import HTTPException
from hashlib import sha256
from pathlib import Path

from starlette.responses import FileResponse


class DataService:
    """
    Serviço que lida com a manipulação de arquivos CSV e ZIP, incluindo a criação de arquivos ZIP
    contendo arquivos CSV e a geração de um hash SHA256 para arquivos ZIP.

    Attributes:
        pasta_csv (Path): O diretório onde os arquivos CSV estão localizados.
        pasta_zip (Path): O diretório onde o arquivo ZIP será armazenado.
    """

    def __init__(self, pasta_csv, pasta_zip):
        """
        Args:
            pasta_csv (str): O caminho para a pasta contendo os arquivos CSV.
            pasta_zip (str): O caminho para a pasta onde o arquivo ZIP será gerado.
        """
        self.pasta_csv = Path(pasta_csv)
        self.pasta_zip = Path(pasta_zip)

    def create_zip(self):
        """
        Cria um arquivo ZIP contendo todos os arquivos CSV da pasta de entrada.

        O método faz o seguinte:
        - Limpa a pasta de destino removendo arquivos antigos.
        - Cria um arquivo ZIP chamado `compact.zip` contendo todos os arquivos CSV presentes na pasta de origem.

        Returns:
            FileResponse: A resposta de arquivo ZIP gerado, para ser enviado ao usuário.

        Raises:
            Exception: Se ocorrer um erro durante o processo de criação do arquivo ZIP.
        """
        # Limpar a pasta de destino para remover os antigos
        for item in self.pasta_zip.iterdir():
            if item.is_dir():
                item.unlink()

        # Criar o arquivo ZIP com os arquivos CSV da pasta de origem
        zip_file = self.pasta_zip / "compact.zip"
        with zipfile.ZipFile(zip_file, "w") as file:
            for arquivo in self.pasta_csv.glob("*.csv"):
                file.write(arquivo, arcname=arquivo.name)

        return FileResponse(
            zip_file, media_type="application/zip", filename=zip_file.name
        )

    def create_hash(self):
        """
        Gera um hash SHA256 para o arquivo ZIP gerado.

        O método calcula o hash SHA256 do arquivo `compact.zip` na pasta de destino.

        Returns:
            dict: Um dicionário contendo o nome do arquivo e o valor do hash SHA256.

        Raises:
            HTTPException: Se o arquivo ZIP ou o diretório não existirem.
        """
        file_name = self.pasta_zip / "compact.zip"

        if not file_name.exists() or not self.pasta_zip.exists():
            raise HTTPException(status_code=404, detail="Arquivo não encontrado")

        hash_fuc = sha256()
        with file_name.open("rb") as file:
            for pedaco in iter(lambda: file.read(4096), b""):
                hash_fuc.update(pedaco)

        return {"arquivo": file_name.name, "hash": hash_fuc.hexdigest()}
