from unittest.mock import patch

import pytest
from fastapi import HTTPException

from packages.v1.administrativo.schemas.p_livro_andamento_schema import PLivroAndamentoIdSchema
from packages.v1.administrativo.services.p_livro_andamento.go.p_livro_andamento_delete_service import (
    DeleteService,
)


@pytest.mark.unit
def test_delete_service_raises_409_when_titulo_linked():
    schema = PLivroAndamentoIdSchema(livro_andamento_id=5)

    with patch(
        "packages.v1.administrativo.services.p_livro_andamento.go.p_livro_andamento_delete_service.ShowAction"
    ) as show_mock, patch(
        "packages.v1.administrativo.services.p_livro_andamento.go.p_livro_andamento_delete_service.CountByTituloRepository"
    ) as count_mock:
        show_mock.return_value.execute.return_value = {"livro_andamento_id": 5}
        count_mock.return_value.execute.return_value = 2

        with pytest.raises(HTTPException) as exc:
            DeleteService().execute(schema)

    assert exc.value.status_code == 409
