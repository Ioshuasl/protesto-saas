import pytest
from pydantic import ValidationError

from packages.v1.administrativo.schemas.p_motivos_cancelamento_schema import (
    PMotivosCancelamentoIndexSchema,
)


@pytest.mark.unit
def test_index_schema_accepts_descricao_filter():
    schema = PMotivosCancelamentoIndexSchema(descricao="judicial")
    assert schema.descricao == "judicial"


@pytest.mark.unit
def test_index_schema_rejects_unknown_filter():
    with pytest.raises(ValidationError):
        PMotivosCancelamentoIndexSchema(descricao="x", situacao="A")


@pytest.mark.unit
def test_index_uses_orm_when_firebird_orm_enabled():
    from unittest.mock import patch

    from actions.data.query_params_parser import Pagination, QueryParams
    from packages.v1.administrativo.repositories.p_motivos_cancelamento.p_motivos_cancelamento_index_repository import (
        IndexRepository,
    )

    repo = IndexRepository()
    schema = PMotivosCancelamentoIndexSchema(descricao="parte")
    query_params = QueryParams(
        pagination=Pagination(page=1, per_page=20),
        sort=None,
        filters=[],
    )

    with patch(
        "packages.v1.administrativo.repositories.p_motivos_cancelamento.p_motivos_cancelamento_index_repository.use_orm_firebird",
        return_value=True,
    ):
        with patch(
            "packages.v1.administrativo.repositories.p_motivos_cancelamento.p_motivos_cancelamento_index_repository.firebird_orm_supports_string_where",
            return_value=True,
        ):
            with patch.object(
                repo, "_execute_orm", return_value={"rows": [], "pagination": {}}
            ) as orm_mock:
                with patch.object(repo, "_execute_sql") as sql_mock:
                    repo.execute(schema, query_params)

    orm_mock.assert_called_once()
    sql_mock.assert_not_called()
