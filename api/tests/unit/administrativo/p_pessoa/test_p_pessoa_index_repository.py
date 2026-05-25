from unittest.mock import patch

import pytest

from packages.v1.administrativo.repositories.p_pessoa.p_pessoa_index_repository import (
    IndexRepository,
    _varchar15_like_prefix,
)


@pytest.mark.unit
def test_varchar15_like_prefix_cnpj_14_digitos():
    assert _varchar15_like_prefix("07158428000106") == "07158428000106%"


@pytest.mark.unit
def test_varchar15_like_prefix_nao_usa_curinga_inicial():
    pattern = _varchar15_like_prefix("07158428000106")
    assert not pattern.startswith("%")
    assert len(pattern) <= 15


@pytest.mark.unit
def test_varchar15_like_prefix_remove_mascara():
    assert _varchar15_like_prefix("07.158.428/0001-06") == "07158428000106%"


@pytest.mark.unit
def test_group_rows_by_cpfcnpj_keeps_latest_pessoa_id_and_ignores_empty_docs():
    rows = [
        {"pessoa_id": 1, "nome": "Sem doc 1", "cpfcnpj": None},
        {"pessoa_id": 2, "nome": "Antigo", "cpfcnpj": "23.651.671/0001-18"},
        {"pessoa_id": 3, "nome": "Sem doc 2", "cpfcnpj": ""},
        {"pessoa_id": 4, "nome": "Recente", "cpfcnpj": "23651671000118"},
    ]

    grouped = IndexRepository._group_rows_by_cpfcnpj(rows)

    assert [row["pessoa_id"] for row in grouped] == [1, 3, 4]


@pytest.mark.unit
def test_enrich_rows_with_total_titulos_sums_duplicate_cpfcnpj_counts():
    repo = IndexRepository()
    rows = [{"pessoa_id": 4, "nome": "Recente", "cpfcnpj": "23651671000118"}]

    with (
        patch.object(
            repo,
            "_fetch_pessoa_ids_by_cpfcnpj_digits",
            return_value={"23651671000118": [2, 4]},
        ),
        patch(
            "packages.v1.administrativo.repositories.p_pessoa.p_pessoa_index_repository.CountTitulosByPessoaIdsRepository"
        ) as mock_count_cls,
    ):
        mock_count_cls.return_value.execute.return_value = {2: 3, 4: 5}
        enriched = repo._enrich_rows_with_total_titulos(rows)

    assert enriched[0]["total_titulos"] == 8


@pytest.mark.unit
@pytest.mark.integration
def test_busca_unificada_cnpj_sem_erro_varchar15():
    from actions.data.query_params_parser import Pagination, QueryParams, Sort
    from packages.v1.administrativo.actions.p_pessoa.p_pessoa_index_action import (
        IndexAction,
    )
    from packages.v1.administrativo.schemas.p_pessoa_schema import PPessoaIndexSchema

    qp = QueryParams(
        pagination=Pagination(page=1, per_page=10),
        sort=Sort(field="pessoa_id", direction="desc"),
        filters=[],
    )
    result = IndexAction().execute(
        PPessoaIndexSchema(busca="07158428000106"),
        qp,
    )
    assert result["pagination"]["total"] >= 0
    assert isinstance(result["rows"], list)
