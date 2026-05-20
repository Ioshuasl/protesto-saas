from packages.v1.administrativo.actions.t_tb_cartorio.t_tb_cartorio_save_action import (
    TTbCartorioSaveAction,
)
from packages.v1.administrativo.schemas.t_tb_cartorio_schema import TTbCartorioSaveSchema
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaSchema
from packages.v1.sequencia.services.g_sequencia.generate_service import GenerateService


class TTbCartorioSaveService:
    def execute(self, cartorio_schema: TTbCartorioSaveSchema):
        if not cartorio_schema.tb_cartorio_id:
            sequencia_schema = GSequenciaSchema(tabela="T_TB_CARTORIO")
            sequencia = GenerateService().execute(sequencia_schema)
            cartorio_schema.tb_cartorio_id = sequencia.sequencia

        return TTbCartorioSaveAction().execute(cartorio_schema)
