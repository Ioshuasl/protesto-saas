from fastapi import HTTPException, status

from packages.v1.administrativo.actions.p_livro_andamento.p_livro_andamento_show_action import (
    ShowAction,
)
from packages.v1.administrativo.actions.p_livro_andamento.p_livro_andamento_update_action import (
    UpdateAction,
)
from packages.v1.administrativo.actions.p_livro_natureza.p_livro_natureza_show_action import (
    ShowAction as NaturezaShowAction,
)
from packages.v1.administrativo.repositories.p_livro_andamento.p_livro_andamento_count_aberto_by_natureza_repository import (
    CountAbertoByNaturezaRepository,
)
from packages.v1.administrativo.schemas.p_livro_andamento_schema import (
    PLivroAndamentoIdSchema,
    PLivroAndamentoUpdateSchema,
    is_livro_aberto,
    normalize_sigla,
)
from packages.v1.administrativo.schemas.p_livro_natureza_schema import PLivroNaturezaIdSchema


class UpdateService:
    @staticmethod
    def _row_value(row, key: str):
        if row is None:
            return None
        return row.get(key) or row.get(key.upper())

    def _load_natureza(self, livro_natureza_id: int) -> dict:
        natureza = NaturezaShowAction().execute(
            PLivroNaturezaIdSchema(livro_natureza_id=livro_natureza_id)
        )
        if not natureza:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Não foi possível localizar a natureza de livro.",
            )
        return natureza

    def _resolve_sigla_on_update(
        self,
        schema: PLivroAndamentoUpdateSchema,
        natureza: dict,
    ) -> None:
        natureza_sigla = normalize_sigla(natureza.get("sigla"))
        if schema.sigla is None:
            schema.sigla = natureza_sigla
            return
        if natureza_sigla and schema.sigla != natureza_sigla:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=[
                    {
                        "input": "sigla",
                        "message": (
                            "A sigla do livro deve ser a mesma da natureza de livro "
                            f"({natureza_sigla})."
                        ),
                    }
                ],
            )

    def execute(
        self, livro_andamento_id: int, livro_andamento_schema: PLivroAndamentoUpdateSchema
    ):
        current = ShowAction().execute(PLivroAndamentoIdSchema(livro_andamento_id=livro_andamento_id))
        if not current:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Não foi possível localizar o livro de andamento.",
            )

        natureza_id = (
            livro_andamento_schema.livro_natureza_id
            if livro_andamento_schema.livro_natureza_id is not None
            else int(self._row_value(current, "livro_natureza_id"))
        )
        natureza = self._load_natureza(natureza_id)
        self._resolve_sigla_on_update(livro_andamento_schema, natureza)

        if "data_fechamento" in livro_andamento_schema.model_fields_set:
            data_fechamento = livro_andamento_schema.data_fechamento
        else:
            data_fechamento = current.get("data_fechamento")

        if is_livro_aberto(data_fechamento):
            abertos = CountAbertoByNaturezaRepository().execute(
                natureza_id, exclude_livro_andamento_id=livro_andamento_id
            )
            if abertos > 0:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=[
                        {
                            "input": "livro_natureza_id",
                            "message": (
                                "Já existe um livro de andamento aberto para esta "
                                "natureza de livro."
                            ),
                        }
                    ],
                )

        return UpdateAction().execute(livro_andamento_id, livro_andamento_schema)
