import pytest
from pydantic import ValidationError

from packages.v1.administrativo.schemas.p_ocorrencias_schema import POcorrenciasIndexSchema


@pytest.mark.unit
def test_index_schema_accepts_busca_filter():
    schema = POcorrenciasIndexSchema(busca="pago")
    assert schema.busca == "pago"


@pytest.mark.unit
def test_index_schema_accepts_tipo_filter():
    schema = POcorrenciasIndexSchema(tipo="CADASTRO")
    assert schema.tipo == "CADASTRO"


@pytest.mark.unit
def test_index_schema_rejects_invalid_tipo():
    with pytest.raises(ValidationError):
        POcorrenciasIndexSchema(tipo="PROTESTO")


@pytest.mark.unit
def test_index_schema_rejects_unknown_filter():
    with pytest.raises(ValidationError):
        POcorrenciasIndexSchema(busca="x", descricao="y")


@pytest.mark.unit
def test_index_uses_orm_when_busca_filter_present():
    from unittest.mock import patch

    from actions.data.query_params_parser import Pagination, QueryParams
    from packages.v1.administrativo.repositories.p_ocorrencias.p_ocorrencias_index_repository import (
        IndexRepository,
    )

    repo = IndexRepository()
    schema = POcorrenciasIndexSchema(busca="1")
    query_params = QueryParams(
        pagination=Pagination(page=1, per_page=20),
        sort=None,
        filters=[],
    )

    with patch(
        "packages.v1.administrativo.repositories.p_ocorrencias.p_ocorrencias_index_repository.use_orm_firebird",
        return_value=True,
    ):
        with patch.object(repo, "_execute_orm", return_value={"rows": [], "pagination": {}}) as orm_mock:
            with patch.object(repo, "_execute_sql") as sql_mock:
                repo.execute(schema, query_params)

    orm_mock.assert_called_once()
    sql_mock.assert_not_called()
