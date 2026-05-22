from unittest.mock import patch

import pytest
from fastapi import HTTPException

from packages.v1.administrativo.schemas.p_ocorrencia_andamento_schema import (
    POcorrenciaAndamentoIdSchema,
)
from packages.v1.administrativo.services.p_ocorrencia_andamento.go.p_ocorrencia_andamento_delete_service import (
    DeleteService,
)


@pytest.mark.unit
def test_delete_service_raises_409_when_titulos_linked():
    schema = POcorrenciaAndamentoIdSchema(ocorrencia_andamento_id=1)

    with patch(
        "packages.v1.administrativo.services.p_ocorrencia_andamento.go.p_ocorrencia_andamento_delete_service.ShowAction"
    ) as show_mock, patch(
        "packages.v1.administrativo.services.p_ocorrencia_andamento.go.p_ocorrencia_andamento_delete_service.CountTitulosRepository"
    ) as count_titulos_mock, patch(
        "packages.v1.administrativo.services.p_ocorrencia_andamento.go.p_ocorrencia_andamento_delete_service.CountAndamentosRepository"
    ) as count_andamentos_mock:
        show_mock.return_value.execute.return_value = {"ocorrencia_andamento_id": 1}
        count_titulos_mock.return_value.execute.return_value = 1
        count_andamentos_mock.return_value.execute.return_value = 0

        with pytest.raises(HTTPException) as exc:
            DeleteService().execute(schema)

    assert exc.value.status_code == 409


@pytest.mark.unit
def test_delete_service_raises_409_when_andamentos_linked():
    schema = POcorrenciaAndamentoIdSchema(ocorrencia_andamento_id=1)

    with patch(
        "packages.v1.administrativo.services.p_ocorrencia_andamento.go.p_ocorrencia_andamento_delete_service.ShowAction"
    ) as show_mock, patch(
        "packages.v1.administrativo.services.p_ocorrencia_andamento.go.p_ocorrencia_andamento_delete_service.CountTitulosRepository"
    ) as count_titulos_mock, patch(
        "packages.v1.administrativo.services.p_ocorrencia_andamento.go.p_ocorrencia_andamento_delete_service.CountAndamentosRepository"
    ) as count_andamentos_mock:
        show_mock.return_value.execute.return_value = {"ocorrencia_andamento_id": 1}
        count_titulos_mock.return_value.execute.return_value = 0
        count_andamentos_mock.return_value.execute.return_value = 3

        with pytest.raises(HTTPException) as exc:
            DeleteService().execute(schema)

    assert exc.value.status_code == 409
