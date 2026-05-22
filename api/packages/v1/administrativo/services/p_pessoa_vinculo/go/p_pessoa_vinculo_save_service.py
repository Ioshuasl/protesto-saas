from fastapi import HTTPException, status

from packages.v1.administrativo.actions.p_pessoa_vinculo.p_pessoa_vinculo_save_action import (
    SaveAction,
)
from packages.v1.administrativo.actions.p_pessoa.p_pessoa_show_action import (
    ShowAction as PessoaShowAction,
)
from packages.v1.administrativo.model.p_titulo import get_p_titulo_model
from packages.v1.administrativo.schemas.p_pessoa_schema import PPessoaIdSchema
from packages.v1.administrativo.schemas.p_pessoa_vinculo_schema import PPessoaVinculoSaveSchema
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaSchema
from packages.v1.sequencia.services.g_sequencia.generate_service import GenerateService


class SaveService:
    def _ensure_titulo_exists(self, titulo_id: int) -> None:
        row = get_p_titulo_model().findByPk(titulo_id)
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=[
                    {
                        "input": "titulo_id",
                        "message": "Título não encontrado.",
                    }
                ],
            )

    def _ensure_pessoa_exists(self, pessoa_id: int) -> None:
        row = PessoaShowAction().execute(PPessoaIdSchema(pessoa_id=pessoa_id))
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=[
                    {
                        "input": "pessoa_id",
                        "message": "Pessoa não encontrada.",
                    }
                ],
            )

    def execute(self, vinculo_schema: PPessoaVinculoSaveSchema):
        self._ensure_titulo_exists(vinculo_schema.titulo_id)
        if vinculo_schema.pessoa_id is not None:
            self._ensure_pessoa_exists(vinculo_schema.pessoa_id)

        if not vinculo_schema.pessoa_vinculo_id:
            sequencia_schema = GSequenciaSchema()
            sequencia_schema.tabela = "P_PESSOA_VINCULO"
            vinculo_schema.pessoa_vinculo_id = GenerateService().execute(
                sequencia_schema
            ).sequencia

        return SaveAction().execute(vinculo_schema)
