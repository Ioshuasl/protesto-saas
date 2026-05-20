import json
import os
from pathlib import Path
from fastapi import HTTPException, status


class File:

    def create(self, data, caminho_arquivo='storage/temp.json'):
        try:
            # Garante que a pasta existe
            os.makedirs(os.path.dirname(caminho_arquivo), exist_ok=True)

            # Lê dados existentes (ou cria nova lista)
            if os.path.exists(caminho_arquivo):
                with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
                    try:
                        dados_existentes = json.load(arquivo)
                        if not isinstance(dados_existentes, list):
                            dados_existentes = []
                    except json.JSONDecodeError:
                        dados_existentes = []
            else:
                dados_existentes = []

            # Adiciona novo dado
            dados_existentes.append(data)

            # Salva novamente no arquivo com indentação
            with open(caminho_arquivo, 'w', encoding='utf-8') as arquivo:
                json.dump(dados_existentes, arquivo, indent=4, ensure_ascii=False)

        except Exception as e:
            print(f"❌ Erro ao salvar o dado: {e}")

    # Lê o conteúdo de um arquivo e retorna o conteúdo binário.
    def read(self, path_file: Path) -> bytes:
        """
        Lê o conteúdo binário de um arquivo.

        :param path_file: Caminho do arquivo (Path)
        :return: Conteúdo em bytes
        """

        # Garante que é um objeto Path
        if not isinstance(path_file, Path):
            path_file = Path(path_file)

        # Verifica se existe
        if not path_file.exists():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Arquivo informado não encontrado.",
            )

        # Verifica se é realmente um arquivo
        if not path_file.is_file():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="O caminho informado não é um arquivo válido.",
            )

        try:
            return path_file.read_bytes()

        except PermissionError:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Sem permissão para acessar o arquivo.",
            )

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao ler o arquivo: {str(e)}",
            )