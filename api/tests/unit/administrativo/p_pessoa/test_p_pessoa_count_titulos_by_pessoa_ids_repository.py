from decimal import Decimal
from unittest.mock import patch

import pytest

from packages.v1.administrativo.repositories.p_pessoa.p_pessoa_count_titulos_by_pessoa_ids_repository import (
    CountTitulosByPessoaIdsRepository,
)


@pytest.mark.unit
def test_count_titulos_returns_empty_for_empty_ids():
    assert CountTitulosByPessoaIdsRepository().execute([]) == {}


@pytest.mark.unit
def test_count_titulos_maps_rows_and_defaults_zero():
    repo = CountTitulosByPessoaIdsRepository()
    with patch.object(
        repo,
        "fetch_all",
        return_value=[
            {"PESSOA_ID": Decimal("1"), "TOTAL": Decimal("5")},
            {"pessoa_id": 3, "total": 2},
        ],
    ):
        result = repo.execute([1, 2, 3])

    assert result == {1: 5, 2: 0, 3: 2}


@pytest.mark.unit
def test_count_titulos_splits_ids_into_firebird_safe_chunks():
    repo = CountTitulosByPessoaIdsRepository()
    ids = list(range(1, 1502))

    with patch.object(repo, "fetch_all", return_value=[]) as fetch_all:
        result = repo.execute(ids)

    assert fetch_all.call_count == 2
    assert result[1] == 0
    assert result[1501] == 0
    first_params = fetch_all.call_args_list[0].args[1]
    second_params = fetch_all.call_args_list[1].args[1]
    assert len(first_params) == 1000
    assert len(second_params) == 501


@pytest.mark.unit
def test_index_enrich_rows_with_total_titulos():
    from packages.v1.administrativo.repositories.p_pessoa.p_pessoa_index_repository import (
        IndexRepository,
    )

    rows = [{"pessoa_id": 1, "nome": "A"}, {"pessoa_id": 2, "nome": "B"}]
    with patch(
        "packages.v1.administrativo.repositories.p_pessoa.p_pessoa_index_repository.CountTitulosByPessoaIdsRepository"
    ) as mock_count_cls:
        mock_count_cls.return_value.execute.return_value = {1: 10, 2: 0}
        enriched = IndexRepository()._enrich_rows_with_total_titulos(rows)

    assert enriched[0]["total_titulos"] == 10
    assert enriched[1]["total_titulos"] == 0
