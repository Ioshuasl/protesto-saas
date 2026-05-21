from fastapi import HTTPException, status

from packages.v1.administrativo.actions.p_livro_andamento.p_livro_andamento_save_action import (
    SaveAction,
)
from packages.v1.administrativo.actions.p_livro_natureza.p_livro_natureza_show_action import (
    ShowAction as NaturezaShowAction,
)
from packages.v1.administrativo.repositories.p_livro_andamento.p_livro_andamento_count_aberto_by_natureza_repository import (
    CountAbertoByNaturezaRepository,
)
from packages.v1.administrativo.schemas.p_livro_andamento_schema import (
    PLivroAndamentoSaveSchema,
    is_livro_aberto,
    normalize_sigla,
)
from packages.v1.administrativo.schemas.p_livro_natureza_schema import PLivroNaturezaIdSchema
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaSchema
from packages.v1.sequencia.services.g_sequencia.generate_service import GenerateService


class SaveService:
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

    def _resolve_sigla(self, schema: PLivroAndamentoSaveSchema, natureza: dict) -> None:
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

    def _ensure_single_aberto(self, livro_natureza_id: int) -> None:
        abertos = CountAbertoByNaturezaRepository().execute(livro_natureza_id)
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

    def execute(self, livro_andamento_schema: PLivroAndamentoSaveSchema):
        natureza = self._load_natureza(livro_andamento_schema.livro_natureza_id)
        self._resolve_sigla(livro_andamento_schema, natureza)

        if is_livro_aberto(livro_andamento_schema.data_fechamento):
            self._ensure_single_aberto(livro_andamento_schema.livro_natureza_id)

        if not livro_andamento_schema.livro_andamento_id:
            sequencia_schema = GSequenciaSchema()
            sequencia_schema.tabela = "P_LIVRO_ANDAMENTO"
            livro_andamento_schema.livro_andamento_id = GenerateService().execute(
                sequencia_schema
            ).sequencia

        return SaveAction().execute(livro_andamento_schema)
