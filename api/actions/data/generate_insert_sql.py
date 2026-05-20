from pydantic import BaseModel
from decimal import Decimal


def generate_insert_sql(
    table_name: str,
    data: BaseModel | dict,
    returning_all: bool = False,
) -> str:
    """
    Gera um comando SQL INSERT seguro para Firebird.
    - Aceita BaseModel (Pydantic) ou dict.
    - Mantém colunas em MAIÚSCULAS e parâmetros em minúsculas (bind).
    - returning_all=True força RETURNING *.
    """

    # Converte o model em dict limpo
    if isinstance(data, BaseModel):
        data_dict = data.model_dump(exclude_unset=True)
    elif isinstance(data, dict):
        data_dict = data
    else:
        raise TypeError("O parâmetro 'data' deve ser um BaseModel ou dict.")

    columns = []
    params = []
    returning_fields = []

    for key, value in data_dict.items():
        column_name = key.upper()

        # Converte Decimal → float
        if isinstance(value, Decimal):
            data_dict[key] = float(value)

        # Campos válidos para retorno
        if value is not None:
            returning_fields.append(column_name)

        columns.append(column_name)
        params.append(f":{key}")

    columns_str = ", ".join(columns)
    params_str = ", ".join(params)

    if returning_all:
        returning_str = "*"
    else:
        returning_str = ", ".join(returning_fields) if returning_fields else "*"

    sql = (
        f"INSERT INTO {table_name} (\n"
        f"    {columns_str}\n"
        f") VALUES (\n"
        f"    {params_str}\n"
        f") RETURNING {returning_str};"
    )

    return sql
