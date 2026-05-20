from typing import Tuple, Dict, Any
from pydantic import BaseModel


def prepare_update_data(
    schema: BaseModel, exclude_fields: list[str] = None, id_field: str = "id"
) -> Tuple[Dict[str, Any], str]:
    """
    Gera dinamicamente os dados e SQL para update com base em um schema Pydantic.

    Args:
        schema: Instância do schema (ex: t_pessoa_save_schema)
        exclude_fields: Lista de campos a serem ignorados no SET (ex: ['pessoa_id'])
        id_field: Nome do campo identificador primário (ex: 'pessoa_id')

    Returns:
        Tuple contendo:
        - data_dict: dicionário com apenas campos preenchidos (sem unset)
        - update_sql: string SQL do tipo "campo1 = :campo1, campo2 = :campo2"
    """
    exclude_fields = exclude_fields or [id_field]

    # Cria o dicionário apenas com os campos enviados
    data_dict = schema.model_dump(exclude_unset=True)

    # Monta lista dinâmica de campos para o SET
    update_fields = [f"{k} = :{k}" for k in data_dict.keys() if k not in exclude_fields]

    update_sql = ", ".join(update_fields)
    return data_dict, update_sql
