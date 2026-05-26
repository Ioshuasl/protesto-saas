from decimal import Decimal
from unittest.mock import patch

import pytest

from actions.data.query_params_parser import Pagination, QueryParams
from packages.v1.administrativo.repositories.p_template.p_template_index_repository import (
    IndexRepository,
)
from packages.v1.administrativo.repositories.p_template.p_template_save_repository import (
    SaveRepository,
)
from packages.v1.administrativo.repositories.p_template.p_template_update_repository import (
    UpdateRepository,
)
from packages.v1.administrativo.schemas.p_template_schema import (
    PTemplateIndexSchema,
    PTemplateSaveSchema,
    PTemplateUpdateSchema,
)


@pytest.mark.unit
def test_index_builds_sql_filters_for_expected_fields():
    schema = PTemplateIndexSchema(template_id=2, descricao="certidao")

    where, params = IndexRepository._build_sql_filters(schema)

    assert "TEMPLATE_ID = :template_id" in where
    assert "UPPER(DESCRICAO) LIKE UPPER(:descricao)" in where
    assert params["template_id"] == 2
    assert params["descricao"] == "%certidao%"


@pytest.mark.unit
def test_index_maps_decimal_and_ignores_blob_texto():
    row = {
        "TEMPLATE_ID": Decimal("2.00"),
        "DESCRICAO": "  Certidão Positiva  ",
        "TEXTO": b"nao deve sair",
    }

    mapped = IndexRepository._map_row(row)

    assert mapped == {
        "template_id": 2,
        "descricao": "Certidão Positiva",
    }
    assert "texto" not in mapped


@pytest.mark.unit
def test_save_builds_payload_without_blob_texto():
    schema = PTemplateSaveSchema(
        template_id=3,
        descricao="Modelo inicial",
    )

    payload = SaveRepository._build_payload(schema)

    assert payload == {
        "TEMPLATE_ID": 3,
        "DESCRICAO": "Modelo inicial",
    }


@pytest.mark.unit
def test_update_builds_payload_without_template_id_or_blob_texto():
    schema = PTemplateUpdateSchema(descricao="Modelo atualizado")

    payload = UpdateRepository._build_payload(schema)

    assert payload == {"DESCRICAO": "Modelo atualizado"}


@pytest.mark.unit
def test_index_uses_orm_when_firebird_orm_enabled():
    repo = IndexRepository()
    schema = PTemplateIndexSchema(descricao="certidao")
    query_params = QueryParams(
        pagination=Pagination(page=1, per_page=20),
        sort=None,
        filters=[],
    )

    with patch(
        "packages.v1.administrativo.repositories.p_template.p_template_index_repository.use_orm_firebird",
        return_value=True,
    ):
        with patch(
            "packages.v1.administrativo.repositories.p_template.p_template_index_repository.firebird_orm_supports_string_where",
            return_value=True,
        ):
            with patch.object(
                repo, "_execute_orm", return_value={"rows": [], "pagination": {}}
            ) as orm_mock:
                with patch.object(repo, "_execute_sql") as sql_mock:
                    repo.execute(schema, query_params)

    orm_mock.assert_called_once()
    sql_mock.assert_not_called()
