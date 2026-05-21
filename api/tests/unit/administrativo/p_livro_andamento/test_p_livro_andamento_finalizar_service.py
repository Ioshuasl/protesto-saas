from datetime import datetime
from unittest.mock import patch

import pytest
from fastapi import HTTPException

from packages.v1.administrativo.schemas.p_livro_andamento_schema import (
    PLivroAndamentoFinalizarSchema,
)
from packages.v1.administrativo.services.p_livro_andamento.go.p_livro_andamento_finalizar_service import (
    FinalizarService,
)


@pytest.mark.unit
def test_finalizar_service_raises_409_when_livro_ja_fechado():
    schema = PLivroAndamentoFinalizarSchema(data_fechamento=datetime(2026, 5, 22))

    with patch(
        "packages.v1.administrativo.services.p_livro_andamento.go.p_livro_andamento_finalizar_service.ShowAction"
    ) as show_mock:
        show_mock.return_value.execute.return_value = {
            "livro_andamento_id": 1,
            "data_abertura": datetime(2026, 5, 21),
            "data_fechamento": datetime(2026, 5, 20),
        }

        with pytest.raises(HTTPException) as exc:
            FinalizarService().execute(1, schema)

    assert exc.value.status_code == 409


@pytest.mark.unit
def test_finalizar_service_raises_422_when_fechamento_antes_abertura():
    schema = PLivroAndamentoFinalizarSchema(data_fechamento=datetime(2026, 5, 20))

    with patch(
        "packages.v1.administrativo.services.p_livro_andamento.go.p_livro_andamento_finalizar_service.ShowAction"
    ) as show_mock:
        show_mock.return_value.execute.return_value = {
            "livro_andamento_id": 1,
            "data_abertura": datetime(2026, 5, 21),
            "data_fechamento": None,
        }

        with pytest.raises(HTTPException) as exc:
            FinalizarService().execute(1, schema)

    assert exc.value.status_code == 422


@pytest.mark.unit
def test_finalizar_service_fecha_livro_aberto():
    schema = PLivroAndamentoFinalizarSchema(
        data_fechamento=datetime(2026, 5, 22),
        folha_atual=50,
    )

    with patch(
        "packages.v1.administrativo.services.p_livro_andamento.go.p_livro_andamento_finalizar_service.ShowAction"
    ) as show_mock, patch(
        "packages.v1.administrativo.services.p_livro_andamento.go.p_livro_andamento_finalizar_service.FinalizarAction"
    ) as finalizar_mock:
        show_mock.return_value.execute.return_value = {
            "livro_andamento_id": 1,
            "data_abertura": datetime(2026, 5, 21),
            "data_fechamento": None,
        }
        finalizar_mock.return_value.execute.return_value = {
            "livro_andamento_id": 1,
            "data_fechamento": datetime(2026, 5, 22),
            "folha_atual": 50,
            "aberto": False,
        }

        result = FinalizarService().execute(1, schema)

    assert result["aberto"] is False
    finalizar_mock.return_value.execute.assert_called_once()
