from datetime import date
from decimal import Decimal
from unittest.mock import patch

import pytest

from actions.data.query_params_parser import Pagination, QueryParams
from packages.v1.administrativo.repositories.p_certidao.p_certidao_index_repository import (
    IndexRepository,
)
from packages.v1.administrativo.services.p_certidao.go.p_certidao_cancelar_service import (
    CancelarService,
)
from packages.v1.administrativo.repositories.p_certidao.p_certidao_save_repository import (
    SaveRepository,
)
from packages.v1.administrativo.schemas.p_certidao_schema import (
    PCertidaoIdSchema,
    PCertidaoIndexSchema,
    PCertidaoSaveSchema,
)


@pytest.mark.unit
def test_index_builds_sql_filters_for_expected_fields():
    schema = PCertidaoIndexSchema(
        tipo_certidao="P",
        data_certidao=date(2026, 5, 26),
        status="A",
        busca="maria",
    )

    where, params = IndexRepository()._build_sql_filters(schema)

    assert "UPPER(TRIM(TIPO_CERTIDAO)) IN ('P', 'N')" in where
    assert "UPPER(TRIM(TIPO_CERTIDAO)) = UPPER(:tipo_certidao)" in where
    assert "CAST(DATA_CERTIDAO AS DATE) = :data_certidao" in where
    assert "UPPER(TRIM(STATUS)) = UPPER(:status)" in where
    assert params["tipo_certidao"] == "P"
    assert params["data_certidao"] == date(2026, 5, 26)
    assert params["status"] == "A"
    assert params["busca"] == "%maria%"


@pytest.mark.unit
def test_index_applies_base_filter_to_hide_serasa_certidoes():
    where, params = IndexRepository()._build_sql_filters(PCertidaoIndexSchema())
    orm_where = IndexRepository._build_orm_where(PCertidaoIndexSchema())

    assert where == ["UPPER(TRIM(TIPO_CERTIDAO)) IN ('P', 'N')"]
    assert params == {}
    assert orm_where


@pytest.mark.unit
def test_index_builds_sql_filters_for_date_range():
    schema = PCertidaoIndexSchema(
        data_inicio=date(2026, 5, 1),
        data_fim=date(2026, 5, 26),
    )

    where, params = IndexRepository()._build_sql_filters(schema)

    assert "CAST(DATA_CERTIDAO AS DATE) >= :data_inicio" in where
    assert "CAST(DATA_CERTIDAO AS DATE) <= :data_fim" in where
    assert params["data_inicio"] == date(2026, 5, 1)
    assert params["data_fim"] == date(2026, 5, 26)


@pytest.mark.unit
def test_index_maps_decimal_and_text_values():
    row = {
        "CERTIDAO_ID": Decimal("10"),
        "USUARIO_ID": "8",
        "VALOR_EMOLUMENTO": "12.345",
        "NOME": "  Pessoa Teste  ",
        "TIPO_CERTIDAO": "p",
        "STATUS": "a",
        "OBSERVACAO": b"observacao",
        "usuario": {"NOME_COMPLETO": "Usuário Certidão", "LOGIN": "ucert"},
    }

    mapped = IndexRepository._map_row(row)

    assert mapped["certidao_id"] == 10
    assert mapped["usuario_id"] == 8
    assert mapped["valor_emolumento"] == 12.345
    assert mapped["nome"] == "Pessoa Teste"
    assert mapped["tipo_certidao"] == "p"
    assert mapped["status"] == "a"
    assert mapped["observacao"] == "observacao"
    assert mapped["usuario_nome"] == "Usuário Certidão"
    assert "usuario" not in mapped


@pytest.mark.unit
def test_save_builds_firebird_payload():
    schema = PCertidaoSaveSchema(
        certidao_id=1,
        tipo_certidao="P",
        status="A",
        nome="Pessoa",
        cpfcnpj="123",
    )

    payload = SaveRepository._build_payload(schema)

    assert payload == {
        "CERTIDAO_ID": 1,
        "TIPO_CERTIDAO": "P",
        "CPFCNPJ": "123",
        "NOME": "Pessoa",
        "STATUS": "A",
    }


@pytest.mark.unit
def test_index_uses_orm_when_firebird_orm_enabled():
    repo = IndexRepository()
    schema = PCertidaoIndexSchema(tipo_certidao="P")
    query_params = QueryParams(
        pagination=Pagination(page=1, per_page=20),
        sort=None,
        filters=[],
    )

    with patch(
        "packages.v1.administrativo.repositories.p_certidao.p_certidao_index_repository.use_orm_firebird",
        return_value=True,
    ):
        with patch(
            "packages.v1.administrativo.repositories.p_certidao.p_certidao_index_repository.firebird_orm_supports_string_where",
            return_value=True,
        ):
            with patch.object(
                repo, "_execute_orm", return_value={"rows": [], "pagination": {}}
            ) as orm_mock:
                with patch.object(repo, "_execute_sql") as sql_mock:
                    repo.execute(schema, query_params)

    orm_mock.assert_called_once()
    sql_mock.assert_not_called()


@pytest.mark.unit
def test_cancelar_service_updates_only_active_certidao():
    schema = PCertidaoIdSchema(certidao_id=10)

    with patch(
        "packages.v1.administrativo.services.p_certidao.go.p_certidao_cancelar_service.ShowAction.execute",
        return_value={"certidao_id": 10, "status": "A"},
    ):
        with patch(
            "packages.v1.administrativo.services.p_certidao.go.p_certidao_cancelar_service.CancelarAction.execute",
            return_value={"certidao_id": 10, "status": "C"},
        ) as cancelar_mock:
            result = CancelarService().execute(schema)

    assert result == {"certidao_id": 10, "status": "C"}
    cancelar_mock.assert_called_once_with(schema)


@pytest.mark.unit
def test_cancelar_service_rejects_non_active_certidao():
    schema = PCertidaoIdSchema(certidao_id=10)

    with patch(
        "packages.v1.administrativo.services.p_certidao.go.p_certidao_cancelar_service.ShowAction.execute",
        return_value={"certidao_id": 10, "status": "C"},
    ):
        with pytest.raises(Exception) as exc_info:
            CancelarService().execute(schema)

    assert getattr(exc_info.value, "status_code", None) == 409
