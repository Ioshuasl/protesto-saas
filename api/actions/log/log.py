import json
import os
from os import PathLike
from typing import Any


class Log:

    @staticmethod
    def register(
        data: Any, caminho_arquivo: str | PathLike[str] = "storage/temp.json"
    ) -> None:
        caminho_arquivo = os.fspath(caminho_arquivo)
        try:
            # Garante que a pasta existe
            os.makedirs(os.path.dirname(caminho_arquivo), exist_ok=True)

            # Lê dados existentes (ou cria nova lista)
            if os.path.exists(caminho_arquivo):
                with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
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
            with open(caminho_arquivo, "w", encoding="utf-8") as arquivo:
                json.dump(dados_existentes, arquivo, indent=4, ensure_ascii=False)

        except Exception as e:
            print(f"❌ Erro ao salvar o dado: {e}")
