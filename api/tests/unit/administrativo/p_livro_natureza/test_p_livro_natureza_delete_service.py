from unittest.mock import patch

import pytest
from fastapi import HTTPException

from packages.v1.administrativo.schemas.p_livro_natureza_schema import PLivroNaturezaIdSchema
from packages.v1.administrativo.services.p_livro_natureza.go.p_livro_natureza_delete_service import (
    DeleteService,
)


@pytest.mark.unit
def test_delete_service_raises_409_when_livro_andamento_linked():
    schema = PLivroNaturezaIdSchema(livro_natureza_id=2)

    with patch(
        "packages.v1.administrativo.services.p_livro_natureza.go.p_livro_natureza_delete_service.ShowAction"
    ) as show_mock, patch(
        "packages.v1.administrativo.services.p_livro_natureza.go.p_livro_natureza_delete_service.CountByLivroNaturezaRepository"
    ) as count_mock:
        show_mock.return_value.execute.return_value = {"livro_natureza_id": 2}
        count_mock.return_value.execute.return_value = 1

        with pytest.raises(HTTPException) as exc:
            DeleteService().execute(schema)

    assert exc.value.status_code == 409
