from datetime import datetime
from unittest.mock import patch

import pytest
from fastapi import HTTPException

from packages.v1.administrativo.schemas.p_livro_andamento_schema import PLivroAndamentoSaveSchema
from packages.v1.administrativo.services.p_livro_andamento.go.p_livro_andamento_save_service import (
    SaveService,
)


def _save_schema(**kwargs) -> PLivroAndamentoSaveSchema:
    defaults = {
        "livro_natureza_id": 1,
        "folha_atual": 1,
        "numero_livro": 1,
        "numero_folhas": 50,
        "data_abertura": datetime(2026, 5, 21),
        "data_fechamento": None,
    }
    defaults.update(kwargs)
    return PLivroAndamentoSaveSchema(**defaults)


@pytest.mark.unit
def test_save_service_raises_409_when_another_livro_aberto():
    schema = _save_schema()

    with patch(
        "packages.v1.administrativo.services.p_livro_andamento.go.p_livro_andamento_save_service.NaturezaShowAction"
    ) as natureza_mock, patch(
        "packages.v1.administrativo.services.p_livro_andamento.go.p_livro_andamento_save_service.CountAbertoByNaturezaRepository"
    ) as count_mock, patch(
        "packages.v1.administrativo.services.p_livro_andamento.go.p_livro_andamento_save_service.GenerateService"
    ), patch(
        "packages.v1.administrativo.services.p_livro_andamento.go.p_livro_andamento_save_service.SaveAction"
    ):
        natureza_mock.return_value.execute.return_value = {
            "livro_natureza_id": 1,
            "sigla": "AP",
        }
        count_mock.return_value.execute.return_value = 1

        with pytest.raises(HTTPException) as exc:
            SaveService().execute(schema)

    assert exc.value.status_code == 409


@pytest.mark.unit
def test_save_service_allows_when_livro_fechado():
    schema = _save_schema(data_fechamento=datetime(2026, 5, 22))

    with patch(
        "packages.v1.administrativo.services.p_livro_andamento.go.p_livro_andamento_save_service.NaturezaShowAction"
    ) as natureza_mock, patch(
        "packages.v1.administrativo.services.p_livro_andamento.go.p_livro_andamento_save_service.CountAbertoByNaturezaRepository"
    ) as count_mock, patch(
        "packages.v1.administrativo.services.p_livro_andamento.go.p_livro_andamento_save_service.GenerateService"
    ) as gen_mock, patch(
        "packages.v1.administrativo.services.p_livro_andamento.go.p_livro_andamento_save_service.SaveAction"
    ) as save_mock:
        natureza_mock.return_value.execute.return_value = {
            "livro_natureza_id": 1,
            "sigla": "AP",
        }
        count_mock.return_value.execute.return_value = 1
        gen_mock.return_value.execute.return_value.sequencia = 99
        save_mock.return_value.execute.return_value = {"livro_andamento_id": 99}

        result = SaveService().execute(schema)

    count_mock.return_value.execute.assert_not_called()
    assert result["livro_andamento_id"] == 99
