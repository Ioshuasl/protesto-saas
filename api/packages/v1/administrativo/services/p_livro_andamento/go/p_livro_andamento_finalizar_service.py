from datetime import datetime

from fastapi import HTTPException, status

from packages.v1.administrativo.actions.p_livro_andamento.p_livro_andamento_finalizar_action import (
    FinalizarAction,
)
from packages.v1.administrativo.actions.p_livro_andamento.p_livro_andamento_show_action import (
    ShowAction,
)
from packages.v1.administrativo.schemas.p_livro_andamento_schema import (
    PLivroAndamentoFinalizarSchema,
    PLivroAndamentoIdSchema,
    PLivroAndamentoUpdateSchema,
    is_livro_aberto,
)


class FinalizarService:
    @staticmethod
    def _parse_data_abertura(value) -> datetime | None:
        if value is None:
            return None
        if isinstance(value, datetime):
            return value.replace(tzinfo=None) if value.tzinfo else value
        if hasattr(value, "year"):
            return datetime.combine(value, datetime.min.time())
        return None

    def execute(
        self,
        livro_andamento_id: int,
        livro_andamento_schema: PLivroAndamentoFinalizarSchema,
    ):
        current = ShowAction().execute(
            PLivroAndamentoIdSchema(livro_andamento_id=livro_andamento_id)
        )
        if not current:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Não foi possível localizar o livro de andamento.",
            )

        if not is_livro_aberto(current.get("data_fechamento")):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=[
                    {
                        "input": "livro_andamento_id",
                        "message": "O livro de andamento já está fechado.",
                    }
                ],
            )

        data_abertura = self._parse_data_abertura(current.get("data_abertura"))
        data_fechamento = livro_andamento_schema.data_fechamento

        if data_abertura and data_fechamento < data_abertura:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=[
                    {
                        "input": "data_fechamento",
                        "message": (
                            "A data de fechamento não pode ser anterior à data de abertura."
                        ),
                    }
                ],
            )

        update_payload: dict = {"data_fechamento": data_fechamento}
        if livro_andamento_schema.folha_atual is not None:
            update_payload["folha_atual"] = livro_andamento_schema.folha_atual
        if livro_andamento_schema.usuario_id is not None:
            update_payload["usuario_id"] = livro_andamento_schema.usuario_id

        update_schema = PLivroAndamentoUpdateSchema(**update_payload)
        return FinalizarAction().execute(livro_andamento_id, update_schema)
