from fastapi import HTTPException, status

from actions.dynamic_import.dynamic_import import DynamicImport
from packages.v1.administrativo.actions.t_tb_sinal_publico.t_tb_sinal_publico_save_action import (
    TTbSinalPublicoSaveAction,
)
from packages.v1.administrativo.schemas.t_tb_sinal_publico_schema import (
    TTbSinalPublicoDescricaoSchema,
    TTbSinalPublicoSaveSchema,
)
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaSchema
from packages.v1.sequencia.services.g_sequencia.generate_service import GenerateService


class TTbSinalPublicoSaveService:
    def __init__(self):
        self.dynamic_import = DynamicImport()
        self.dynamic_import.set_package("administrativo")
        self.dynamic_import.set_table("t_tb_sinal_publico")

    def execute(self, sinal_publico_schema: TTbSinalPublicoSaveSchema):
        descricao_service = self.dynamic_import.service(
            "t_tb_sinal_publico_get_descricao_service",
            "TTbSinalPublicoGetByDescricaoService",
        )
        self.descricao_service = descricao_service()

        response = self.descricao_service.execute(
            TTbSinalPublicoDescricaoSchema(descricao=sinal_publico_schema.descricao),
            False,
        )

        if response:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=[{"input": "descricao", "message": "a descricao informada ja esta sendo utilizada."}],
            )

        if not sinal_publico_schema.tb_sinalpublico_id:
            sequencia_schema = GSequenciaSchema(tabela="T_TB_SINALPUBLICO")
            generate = GenerateService()
            sequencia = generate.execute(sequencia_schema)
            sinal_publico_schema.tb_sinalpublico_id = sequencia.sequencia

        save_action = TTbSinalPublicoSaveAction()
        return save_action.execute(sinal_publico_schema)
