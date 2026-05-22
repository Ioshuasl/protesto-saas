import pytest
from pydantic import ValidationError

from packages.v1.administrativo.schemas.p_motivos_schema import PMotivosIndexSchema


@pytest.mark.unit
def test_index_schema_accepts_descricao_filter():
    schema = PMotivosIndexSchema(descricao="pagamento")
    assert schema.descricao == "pagamento"


@pytest.mark.unit
def test_index_schema_accepts_situacao_filter():
    schema = PMotivosIndexSchema(situacao="A")
    assert schema.situacao == "A"


@pytest.mark.unit
def test_index_schema_rejects_invalid_situacao():
    with pytest.raises(ValidationError):
        PMotivosIndexSchema(situacao="X")


@pytest.mark.unit
def test_index_schema_rejects_unknown_filter():
    with pytest.raises(ValidationError):
        PMotivosIndexSchema(descricao="x", codigo="1")


@pytest.mark.unit
def test_index_uses_orm_when_situacao_filter_present():
    from unittest.mock import patch

    from actions.data.query_params_parser import Pagination, QueryParams
    from packages.v1.administrativo.repositories.p_motivos.p_motivos_index_repository import (
        IndexRepository,
    )

    repo = IndexRepository()
    schema = PMotivosIndexSchema(situacao="I")
    query_params = QueryParams(
        pagination=Pagination(page=1, per_page=20),
        sort=None,
        filters=[],
    )

    with patch(
        "packages.v1.administrativo.repositories.p_motivos.p_motivos_index_repository.use_orm_firebird",
        return_value=True,
    ):
        with patch.object(repo, "_execute_orm", return_value={"rows": [], "pagination": {}}) as orm_mock:
            with patch.object(repo, "_execute_sql") as sql_mock:
                repo.execute(schema, query_params)

    orm_mock.assert_called_once()
    sql_mock.assert_not_called()


@pytest.mark.unit
def test_index_uses_orm_when_firebird_orm_enabled():
    from unittest.mock import patch

    from actions.data.query_params_parser import Pagination, QueryParams
    from packages.v1.administrativo.repositories.p_motivos.p_motivos_index_repository import (
        IndexRepository,
    )

    repo = IndexRepository()
    schema = PMotivosIndexSchema(descricao="pagamento")
    query_params = QueryParams(
        pagination=Pagination(page=1, per_page=20),
        sort=None,
        filters=[],
    )

    with patch(
        "packages.v1.administrativo.repositories.p_motivos.p_motivos_index_repository.use_orm_firebird",
        return_value=True,
    ):
        with patch(
            "packages.v1.administrativo.repositories.p_motivos.p_motivos_index_repository.firebird_orm_supports_string_where",
            return_value=True,
        ):
            with patch.object(
                repo, "_execute_orm", return_value={"rows": [], "pagination": {}}
            ) as orm_mock:
                with patch.object(repo, "_execute_sql") as sql_mock:
                    repo.execute(schema, query_params)

    orm_mock.assert_called_once()
    sql_mock.assert_not_called()
