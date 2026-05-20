from fastapi import HTTPException, status

from packages.v1.administrativo.actions.t_pessoa_sinal_publico.t_pessoa_sinal_publico_delete_action import (
    TPessoaSinalPublicoDeleteAction,
)
from packages.v1.administrativo.actions.t_pessoa_sinal_publico.t_pessoa_sinal_publico_show_action import (
    TPessoaSinalPublicoShowAction,
)
from packages.v1.administrativo.schemas.t_pessoa_sinal_publico_schema import (
    TPessoaSinalPublicoIdSchema,
)
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaDeleteSchema
from packages.v1.sequencia.services.g_sequencia.delete_service import (
    DeleteService as SequenciaDeleteService,
)


class TPessoaSinalPublicoDeleteService:
    def execute(self, pessoa_sinal_publico_schema: TPessoaSinalPublicoIdSchema):
        show_action = TPessoaSinalPublicoShowAction()
        current_data = show_action.execute(pessoa_sinal_publico_schema)

        if not current_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nao foi possivel localizar o registro de pessoa sinal publico",
            )

        delete_action = TPessoaSinalPublicoDeleteAction()
        data = delete_action.execute(pessoa_sinal_publico_schema)

        if not data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nao foi possivel excluir o registro ou ele nao existe.",
            )

        seq_service = SequenciaDeleteService()
        seq_service.execute(
            GSequenciaDeleteSchema(
                sequencia=pessoa_sinal_publico_schema.pessoa_sinalpublico_id,
                tabela="T_PESSOA_SINALPUBLICO",
            )
        )

        return data
