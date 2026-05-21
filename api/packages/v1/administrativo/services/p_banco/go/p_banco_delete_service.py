from fastapi import HTTPException, status

from packages.v1.administrativo.actions.p_banco.p_banco_delete_action import DeleteAction
from packages.v1.administrativo.actions.p_banco.p_banco_show_action import ShowAction
from packages.v1.administrativo.repositories.p_titulo.p_titulo_count_by_banco_repository import (
    CountByBancoRepository as CountTituloRepository,
)
from packages.v1.administrativo.schemas.p_banco_schema import PBancoIdSchema
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaDeleteSchema
from packages.v1.sequencia.services.g_sequencia.delete_service import (
    DeleteService as SequenciaDeleteService,
)


class DeleteService:
    def execute(self, banco_schema: PBancoIdSchema):
        current = ShowAction().execute(banco_schema)
        if not current:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Não foi possível localizar o banco.",
            )

        titulos = CountTituloRepository().execute(banco_schema)
        if titulos > 0:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=[
                    {
                        "input": "banco_id",
                        "message": "Não é possível remover o banco: existem títulos vinculados.",
                    }
                ],
            )

        data = DeleteAction().execute(banco_schema)

        if data:
            seq_service = SequenciaDeleteService()
            sequencia_schema = GSequenciaDeleteSchema(
                sequencia=banco_schema.banco_id,
                tabela="P_BANCO",
            )
            seq_service.execute(sequencia_schema)

        return data
