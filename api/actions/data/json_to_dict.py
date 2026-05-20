import json
from pathlib import Path
from typing import Any, Union


class JsonToDict:
    """
    Converte conteúdo JSON (string, bytes ou arquivo) em dicionário Python.
    """

    @staticmethod
    def parse(data: Union[str, bytes, Path]) -> dict[str, Any]:
        """
        Recebe uma string JSON, bytes ou caminho de arquivo .json
        e retorna um dicionário Python.
        """

        try:
            # Caso seja um caminho de arquivo
            if isinstance(data, Path):
                with open(data, "r", encoding="utf-8") as file:
                    return json.load(file)

            # Caso seja conteúdo JSON (str ou bytes)
            if isinstance(data, bytes):
                data = data.decode("utf-8")

            # Garante que é string JSON
            if isinstance(data, str):
                return json.loads(data)

            raise TypeError("Tipo de entrada inválido. Use str, bytes ou Path.")

        except json.JSONDecodeError as e:
            raise ValueError(f"Erro ao decodificar JSON: {e}")
        except Exception as e:
            raise ValueError(f"Erro ao converter JSON para dict: {e}")
