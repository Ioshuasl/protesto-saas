from datetime import datetime

from packages.v1.servicos.atos.actions.t_ato_parteimovel.t_ato_parteimovel_delete_action import (
    TAtoParteImovelDeleteAction,
)
from packages.v1.servicos.atos.actions.t_ato_parteimovel.t_ato_parteimovel_show_action import (
    TAtoParteImovelShowAction,
)
from packages.v1.servicos.atos.schemas.t_historico_schema import THistoricoSaveSchema
from packages.v1.servicos.atos.schemas.t_ato_parteimovel_schema import (
    TAtoParteImovelIdSchema,
)
from packages.v1.servicos.atos.services.t_historico.go.t_historico_save_service import (
    THistoricoSaveService,
)
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaDeleteSchema
from packages.v1.sequencia.services.g_sequencia.delete_service import (
    DeleteService as SequenciaDeleteService,
)


class TAtoParteImovelDeleteService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de exclusão de um registro na tabela T_ATO_PARTEIMOVEL.
    """

    def execute(
        self,
        t_ato_parteimovel_id_schema: TAtoParteImovelIdSchema,
    ):
        """
        Executa a operação de exclusão do registro no banco de dados.

        Args:
            t_ato_parteimovel_id_schema (TAtoParteImovelIdSchema):
                O esquema com o ID do registro a ser excluído.

        Returns:
            O resultado da operação de exclusão.
        """
        # ----------------------------------------------------
        # Instanciamento da ação
        # ----------------------------------------------------
        t_ato_parteimovel_delete_action = TAtoParteImovelDeleteAction()

        # ----------------------------------------------------
        # Valida existência (e levanta 404 se não existir)
        # ----------------------------------------------------
        show_action = TAtoParteImovelShowAction()
        show_action.execute(t_ato_parteimovel_id_schema)

        # ----------------------------------------------------
        # Execução da ação
        # ----------------------------------------------------
        data = t_ato_parteimovel_delete_action.execute(t_ato_parteimovel_id_schema)

        # ----------------------------------------------------
        # Controle de sequência após delete
        # ----------------------------------------------------
        seq_service = SequenciaDeleteService()
        sequencia_schema = GSequenciaDeleteSchema(
            sequencia=int(t_ato_parteimovel_id_schema.ato_parteimovel_id),
            tabela="T_ATO_PARTEIMOVEL",
        )
        seq_service.execute(sequencia_schema)

        # ----------------------------------------------------
        # Grava histórico de exclusão da parte/imóvel
        # ----------------------------------------------------
        now = datetime.now()
        now_br = now.strftime("%d/%m/%Y %H:%M:%S")
        usuario_id = t_ato_parteimovel_id_schema.usuario_id
        ato_parteimovel_id = t_ato_parteimovel_id_schema.ato_parteimovel_id

        historico_schema = THistoricoSaveSchema(
            tabela="T_ATO_PARTEIMOVEL",
            campo="Exclusão de parte/imóvel",
            operacao="E",
            new_value=None,
            usuario_id=usuario_id,
            data=now,
            id=ato_parteimovel_id,
            observacao=f"Parte/imóvel removido pelo usuário({usuario_id}), no dia {now_br}",
            data_registro=None,
            dados_complementares=None,
        )

        t_historico_save_service = THistoricoSaveService()
        t_historico_save_service.execute(historico_schema)

        # ----------------------------------------------------
        # Retorno da informação
        # ----------------------------------------------------
        return data
