from datetime import datetime

from packages.v1.servicos.atos.actions.t_ato_vinculoimovel.t_ato_vinculoimovel_save_action import (
    TAtoVinculoImovelSaveAction,
)
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaSchema
from packages.v1.servicos.atos.schemas.t_historico_schema import THistoricoSaveSchema
from packages.v1.servicos.atos.schemas.t_ato_vinculoimovel_schema import (
    TAtoVinculoImovelSaveSchema,
)
from packages.v1.servicos.atos.services.t_historico.go.t_historico_save_service import (
    THistoricoSaveService,
)
from packages.v1.sequencia.services.g_sequencia.generate_service import GenerateService


class TAtoVinculoImovelSaveService:

    def execute(self, t_ato_vinculoimovel_save_schema: TAtoVinculoImovelSaveSchema):

        # ----------------------------------------------------
        # Geração automática de ID (sequência)
        # ----------------------------------------------------
        if not t_ato_vinculoimovel_save_schema.ato_vinculoimovel_id:

            # Cria o schema de sequência
            sequencia_schema = GSequenciaSchema()

            sequencia_schema.tabela = "T_ATO_VINCULOIMOVEL"

            # Gera a sequência atualizada
            generate = GenerateService()
            sequencia = generate.execute(sequencia_schema)

            # Atualiza o ID no schema
            t_ato_vinculoimovel_save_schema.ato_vinculoimovel_id = sequencia.sequencia

        # Instancia da classe
        t_ato_vinculoimovel_save_action = TAtoVinculoImovelSaveAction()

        ato_vinculoimovel_response = t_ato_vinculoimovel_save_action.execute(
            t_ato_vinculoimovel_save_schema
        )

        # ----------------------------------------------------
        # Grava histórico de inclusão do vínculo de imóvel
        # ----------------------------------------------------
        now = datetime.now()
        now_br = now.strftime("%d/%m/%Y %H:%M:%S")
        usuario_id = t_ato_vinculoimovel_save_schema.usuario_id
        ato_vinculoimovel_id = getattr(
            ato_vinculoimovel_response,
            "ato_vinculoimovel_id",
            t_ato_vinculoimovel_save_schema.ato_vinculoimovel_id,
        )

        historico_schema = THistoricoSaveSchema(
            tabela="T_ATO_VINCULOIMOVEL",
            campo="Cadastro de vínculo de imóvel",
            operacao="I",
            new_value=None,
            usuario_id=usuario_id,
            data=now,
            id=ato_vinculoimovel_id,
            observacao=f"Vínculo de imóvel cadastrado pelo usuário({usuario_id}), no dia {now_br}",
            data_registro=None,
            dados_complementares=None,
        )

        t_historico_save_service = THistoricoSaveService()
        t_historico_save_service.execute(historico_schema)

        # Retorna o resultado da operação
        return ato_vinculoimovel_response
