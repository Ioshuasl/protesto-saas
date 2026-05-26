from datetime import date
from decimal import Decimal
from unittest.mock import patch

import pytest

from packages.v1.administrativo.repositories.p_certidao.p_certidao_consulta_apresentante_repository import (
    ConsultaApresentanteRepository,
    _digits_only,
)
from packages.v1.administrativo.schemas.p_certidao_schema import (
    PCertidaoConsultaApresentanteSchema,
)


@pytest.mark.unit
def test_consulta_apresentante_schema_sanitizes_required_text():
    schema = PCertidaoConsultaApresentanteSchema(
        apresentante="  Maria Silva  ",
        cpfcnpj="  123.456.789-00  ",
    )

    assert schema.apresentante == "Maria Silva"
    assert schema.cpfcnpj == "123.456.789-00"


@pytest.mark.unit
def test_digits_only_keeps_only_numbers():
    assert _digits_only("12.345.678/0001-90") == "12345678000190"


@pytest.mark.unit
def test_consulta_uses_document_and_name_queries_with_protesto_filter():
    repo = ConsultaApresentanteRepository()
    schema = PCertidaoConsultaApresentanteSchema(
        apresentante="Maria Silva",
        cpfcnpj="123.456.789-00",
        data_inicio=date(2026, 1, 1),
        data_fim=date(2026, 1, 31),
    )

    with patch.object(repo, "fetch_all", return_value=[]) as fetch_all:
        result = repo.execute(schema)

    assert result == {"titulosPorDocumento": [], "candidatosHomonimia": []}
    assert fetch_all.call_count == 2

    document_sql, document_params = fetch_all.call_args_list[0].args
    name_sql, name_params = fetch_all.call_args_list[1].args

    assert "t.DATA_PROTESTO IS NOT NULL" in document_sql
    assert "CAST(t.DATA_PROTESTO AS DATE) >= :data_inicio" in document_sql
    assert "CAST(t.DATA_PROTESTO AS DATE) <= :data_fim" in document_sql
    assert "P_PESSOA_VINCULO v" in document_sql
    assert "P_TITULO t" in document_sql
    assert "P_PESSOA p" in document_sql
    assert document_params["cpfcnpj"] == "12345678900"
    assert document_params["data_inicio"] == date(2026, 1, 1)
    assert document_params["data_fim"] == date(2026, 1, 31)

    assert "LIKE UPPER(:apresentante)" in name_sql
    assert name_params["apresentante"] == "%Maria Silva%"


@pytest.mark.unit
def test_consulta_maps_rows_and_dedupes_document_and_homonym_results():
    repo = ConsultaApresentanteRepository()
    schema = PCertidaoConsultaApresentanteSchema(
        apresentante="Maria Silva",
        cpfcnpj="12345678900",
    )

    document_row = {
        "TITULO_ID": Decimal("10"),
        "PESSOA_VINCULO_ID": Decimal("20"),
        "NUMERO_APONTAMENTO": Decimal("100"),
        "VALOR_TITULO": Decimal("250.50"),
        "NUMERO_TITULO": " A-10 ",
        "TIPO_VINCULO": "DEVEDOR",
        "DEVEDOR_NOME": " Maria Silva ",
        "DEVEDOR_CPFCNPJ": "12345678900",
        "CREDOR_NOME": " Credor Teste ",
        "DATA_PAGO": "2026-01-10",
        "DATA_CANCELAMENTO": None,
    }
    homonym_row = {
        **document_row,
        "TITULO_ID": Decimal("11"),
        "PESSOA_VINCULO_ID": Decimal("21"),
        "DEVEDOR_CPFCNPJ": "99999999999",
    }

    with patch.object(
        repo,
        "fetch_all",
        side_effect=[
            [document_row, document_row],
            [homonym_row, document_row],
        ],
    ):
        result = repo.execute(schema)

    assert len(result["titulosPorDocumento"]) == 1
    assert len(result["candidatosHomonimia"]) == 1
    assert result["titulosPorDocumento"][0]["titulo_id"] == 10
    assert result["titulosPorDocumento"][0]["valor_titulo"] == 250.5
    assert result["titulosPorDocumento"][0]["devedor_nome"] == "Maria Silva"
    assert result["titulosPorDocumento"][0]["credor_nome"] == "Credor Teste"
    assert result["titulosPorDocumento"][0]["status_descricao"] == "Pago"
    assert result["titulosPorDocumento"][0]["vinculos_partes"] == [
        {
            "pessoa_vinculo_id": 20,
            "tipo": "DEVEDOR",
            "descricao": "DEVEDOR",
            "nome": "Maria Silva",
            "cpfcnpj": "12345678900",
        }
    ]
    assert result["candidatosHomonimia"][0]["titulo_id"] == 11


@pytest.mark.unit
def test_consulta_maps_cancelado_status_before_pago():
    row = {
        "TITULO_ID": Decimal("10"),
        "PESSOA_VINCULO_ID": Decimal("20"),
        "DATA_PAGO": "2026-01-10",
        "DATA_CANCELAMENTO": "2026-01-15",
    }

    mapped = ConsultaApresentanteRepository._map_row(row)

    assert mapped["status_descricao"] == "Cancelado"
