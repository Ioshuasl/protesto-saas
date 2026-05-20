from datetime import datetime

from packages.v1.servicos.atos.actions.t_ato_vinculovalor.t_ato_vinculovalor_delete_action import (
    TAtoVinculoValorDeleteAction,
)
from packages.v1.servicos.atos.actions.t_ato_vinculovalor.t_ato_vinculovalor_show_action import (
    TAtoVinculoValorShowAction,
)
from packages.v1.servicos.atos.schemas.t_historico_schema import THistoricoSaveSchema
from packages.v1.servicos.atos.schemas.t_ato_vinculovalor_schema import (
    TAtoVinculoValorIdSchema,
)
from packages.v1.servicos.atos.services.t_historico.go.t_historico_save_service import (
    THistoricoSaveService,
)
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaDeleteSchema
from packages.v1.sequencia.services.g_sequencia.delete_service import (
    DeleteService as SequenciaDeleteService,
)


class TAtoVinculoValorDeleteService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de exclusão de um registro na tabela T_ATO_VINCULOVALOR.
    """

    def execute(
        self,
        t_ato_vinculovalor_id_schema: TAtoVinculoValorIdSchema,
    ):
        """
        Executa a operação de exclusão do registro no banco de dados.

        Args:
            t_ato_vinculovalor_id_schema (TAtoVinculoValorIdSchema):
                O esquema com o ID do registro a ser excluído.

        Returns:
            O resultado da operação de exclusão.
        """
        # ----------------------------------------------------
        # Instanciamento da ação
        # ----------------------------------------------------
        t_ato_vinculovalor_delete_action = TAtoVinculoValorDeleteAction()

        # ----------------------------------------------------
        # Valida existência (e levanta 404 se não existir)
        # ----------------------------------------------------
        show_action = TAtoVinculoValorShowAction()
        show_action.execute(t_ato_vinculovalor_id_schema)

        # ----------------------------------------------------
        # Execução da ação
        # ----------------------------------------------------
        data = t_ato_vinculovalor_delete_action.execute(t_ato_vinculovalor_id_schema)

        # ----------------------------------------------------
        # Controle de sequência após delete
        # ----------------------------------------------------
        seq_service = SequenciaDeleteService()
        sequencia_schema = GSequenciaDeleteSchema(
            sequencia=int(t_ato_vinculovalor_id_schema.ato_vinculovalor_id),
            tabela="T_ATO_VINCULOVALOR",
        )
        seq_service.execute(sequencia_schema)

        # ----------------------------------------------------
        # Grava histórico de exclusão do vínculo de valor
        # ----------------------------------------------------
        now = datetime.now()
        now_br = now.strftime("%d/%m/%Y %H:%M:%S")
        usuario_id = t_ato_vinculovalor_id_schema.usuario_id
        ato_vinculovalor_id = t_ato_vinculovalor_id_schema.ato_vinculovalor_id

        historico_schema = THistoricoSaveSchema(
            tabela="T_ATO_VINCULOVALOR",
            campo="Exclusão de vínculo de valor",
            operacao="E",
            new_value=None,
            usuario_id=usuario_id,
            data=now,
            id=ato_vinculovalor_id,
            observacao=f"Vínculo de valor removido pelo usuário({usuario_id}), no dia {now_br}",
            data_registro=None,
            dados_complementares=None,
        )

        t_historico_save_service = THistoricoSaveService()
        t_historico_save_service.execute(historico_schema)

        # ----------------------------------------------------
        # Retorno da informação
        # ----------------------------------------------------
        return data
