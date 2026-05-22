from decimal import Decimal
from unittest.mock import MagicMock, patch

import pytest

from packages.v1.administrativo.repositories.p_motivos.p_motivos_count_titulos_by_motivos_ids_repository import (
    CountTitulosByMotivosIdsRepository,
)


@pytest.mark.unit
def test_count_titulos_returns_empty_for_empty_ids():
    assert CountTitulosByMotivosIdsRepository().execute([]) == {}


@pytest.mark.unit
def test_count_titulos_maps_rows_and_defaults_zero():
    repo = CountTitulosByMotivosIdsRepository()
    with patch.object(repo, "fetch_all", return_value=[
        {"MOTIVOS_ID": Decimal("1"), "TOTAL": Decimal("15210")},
        {"motivos_id": 3, "total": 2},
    ]):
        result = repo.execute([1, 2, 3])

    assert result == {1: 15210, 2: 0, 3: 2}


@pytest.mark.unit
def test_index_enrich_rows_with_total_titulos():
    from packages.v1.administrativo.repositories.p_motivos.p_motivos_index_repository import (
        IndexRepository,
    )

    rows = [{"motivos_id": 1, "descricao": "A"}, {"motivos_id": 2, "descricao": "B"}]
    with patch(
        "packages.v1.administrativo.repositories.p_motivos.p_motivos_index_repository.CountTitulosByMotivosIdsRepository"
    ) as mock_count_cls:
        mock_count_cls.return_value.execute.return_value = {1: 10, 2: 0}
        enriched = IndexRepository()._enrich_rows_with_total_titulos(rows)

    assert enriched[0]["total_titulos"] == 10
    assert enriched[1]["total_titulos"] == 0
