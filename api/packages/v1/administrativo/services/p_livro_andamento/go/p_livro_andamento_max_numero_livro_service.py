from fastapi import HTTPException, status

from packages.v1.administrativo.actions.p_livro_andamento.p_livro_andamento_max_numero_livro_action import (
    MaxNumeroLivroAction,
)
from packages.v1.administrativo.actions.p_livro_natureza.p_livro_natureza_show_action import (
    ShowAction as NaturezaShowAction,
)
from packages.v1.administrativo.schemas.p_livro_andamento_schema import (
    PLivroAndamentoNaturezaIdSchema,
)
from packages.v1.administrativo.schemas.p_livro_natureza_schema import PLivroNaturezaIdSchema


class MaxNumeroLivroService:
    def execute(self, schema: PLivroAndamentoNaturezaIdSchema) -> dict[str, int]:
        natureza = NaturezaShowAction().execute(
            PLivroNaturezaIdSchema(livro_natureza_id=schema.livro_natureza_id)
        )
        if not natureza:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Não foi possível localizar a natureza de livro.",
            )

        return MaxNumeroLivroAction().execute(schema)
