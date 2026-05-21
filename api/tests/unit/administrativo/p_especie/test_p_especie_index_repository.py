from unittest.mock import MagicMock, patch

import pytest

from packages.v1.administrativo.repositories.p_especie.p_especie_index_repository import (
    IndexRepository,
)
from packages.v1.administrativo.schemas.p_especie_schema import PEspecieIndexSchema


@pytest.mark.unit
def test_busca_merged_deduplicates_by_especie_id():
    repo = IndexRepository()
    repo._fetch_by_especie_sigla = MagicMock(
        return_value=[{"ESPECIE_ID": 1, "ESPECIE": "DMI", "DESCRICAO": "Duplicata"}]
    )
    repo._fetch_by_descricao = MagicMock(
        return_value=[{"ESPECIE_ID": 1, "ESPECIE": "DMI", "DESCRICAO": "Duplicata Mercantil"}]
    )

    result = repo._execute_busca_merged(
        PEspecieIndexSchema(busca="DMI"),
        page=1,
        per_page=20,
        sort_field="ESPECIE_ID",
        sort_direction="DESC",
    )

    assert result["pagination"]["total"] == 1
    assert len(result["rows"]) == 1
    assert result["rows"][0]["especie"] == "DMI"
    repo._fetch_by_especie_sigla.assert_called_once_with("DMI")
    repo._fetch_by_descricao.assert_called_once_with("DMI")


@pytest.mark.unit
def test_sort_rows_desc_by_especie_id():
    rows = [
        {"especie_id": 1, "especie": "A", "descricao": "A"},
        {"especie_id": 3, "especie": "C", "descricao": "C"},
        {"especie_id": 2, "especie": "B", "descricao": "B"},
    ]
    sorted_rows = IndexRepository._sort_rows(rows, "ESPECIE_ID", "DESC")
    assert [r["especie_id"] for r in sorted_rows] == [3, 2, 1]
