from fastapi import HTTPException, status

from packages.v1.administrativo.actions.p_banco.p_banco_save_action import SaveAction
from packages.v1.administrativo.repositories.p_banco.p_banco_get_by_codigo_repository import (
    GetByCodigoRepository,
)
from packages.v1.administrativo.repositories.p_banco.p_banco_layout_exists_repository import (
    LayoutExistsRepository,
)
from packages.v1.administrativo.schemas.p_banco_schema import (
    PBancoCodigoSchema,
    PBancoLayoutIdSchema,
    PBancoSaveSchema,
)
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaSchema
from packages.v1.sequencia.services.g_sequencia.generate_service import GenerateService


class SaveService:
    def _ensure_codigo_unique(self, codigo_banco: str, banco_id: int | None = None):
        duplicate = GetByCodigoRepository().execute(
            PBancoCodigoSchema(codigo_banco=codigo_banco, banco_id=banco_id)
        )
        if duplicate:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=[
                    {
                        "input": "codigo_banco",
                        "message": "Já existe banco cadastrado com este código.",
                    }
                ],
            )

    def _ensure_layout_exists(self, layout_id: int):
        if not LayoutExistsRepository().execute(PBancoLayoutIdSchema(layout_id=layout_id)):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=[
                    {
                        "input": "layout_id",
                        "message": "Layout informado não foi encontrado.",
                    }
                ],
            )

    def execute(self, banco_schema: PBancoSaveSchema):
        self._ensure_codigo_unique(banco_schema.codigo_banco)
        self._ensure_layout_exists(banco_schema.layout_id)

        if not banco_schema.banco_id:
            sequencia_schema = GSequenciaSchema()
            sequencia_schema.tabela = "P_BANCO"
            banco_schema.banco_id = GenerateService().execute(sequencia_schema).sequencia

        return SaveAction().execute(banco_schema)
