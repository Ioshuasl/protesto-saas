from fastapi import HTTPException, status

from packages.v1.administrativo.actions.p_especie.p_especie_delete_action import DeleteAction
from packages.v1.administrativo.actions.p_especie.p_especie_show_action import ShowAction
from packages.v1.administrativo.repositories.p_titulo.p_titulo_count_by_especie_repository import (
    CountByEspecieRepository,
)
from packages.v1.administrativo.schemas.p_especie_schema import PEspecieIdSchema
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaDeleteSchema
from packages.v1.sequencia.services.g_sequencia.delete_service import (
    DeleteService as SequenciaDeleteService,
)


class DeleteService:
    def execute(self, especie_schema: PEspecieIdSchema):
        current = ShowAction().execute(especie_schema)
        if not current:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Não foi possível localizar a espécie.",
            )

        titulos = CountByEspecieRepository().execute(especie_schema)
        if titulos > 0:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=[
                    {
                        "input": "especie_id",
                        "message": "Não é possível remover a espécie: existem títulos vinculados.",
                    }
                ],
            )

        data = DeleteAction().execute(especie_schema)

        if data:
            seq_service = SequenciaDeleteService()
            sequencia_schema = GSequenciaDeleteSchema(
                sequencia=especie_schema.especie_id,
                tabela="P_ESPECIE",
            )
            seq_service.execute(sequencia_schema)

        return data
