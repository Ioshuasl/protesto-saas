from datetime import datetime

from packages.v1.sequencia.schemas.g_sequencia import GSequenciaSchema
from packages.v1.sequencia.services.g_sequencia.generate_service import GenerateService
from packages.v1.servicos.atos.actions.t_ato.t_ato_save_action import (
    TAtoSaveAction,
)
from packages.v1.servicos.atos.schemas.t_ato_schema import TAtoSaveSchema
from packages.v1.servicos.atos.schemas.t_historico_schema import THistoricoSaveSchema
from packages.v1.servicos.atos.services.t_historico.go.t_historico_save_service import (
    THistoricoSaveService,
)


class TAtoSaveService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de criação de registros na tabela T_ATO.
    """

    def execute(self, t_ato_save_schema: TAtoSaveSchema):
        """
        Executa a operação de salvamento do registro no banco de dados.

        Args:
            t_ato_save_schema (TAtoSaveSchema):
                O esquema com os dados a serem salvos.

        Returns:
            O registro recém-criado.
        """

        # ----------------------------------------------------
        # Geração automática de ID (sequência)
        # ----------------------------------------------------
        if not t_ato_save_schema.ato_id:
            # Cria o schema de sequência
            sequencia_schema = GSequenciaSchema()
            sequencia_schema.tabela = "T_ATO"

            # Gera a sequência atualizada
            generate = GenerateService()
            sequencia = generate.execute(sequencia_schema)

            # Atualiza o ID no schema
            t_ato_save_schema.ato_id = sequencia.sequencia

        # ----------------------------------------------------
        # Instanciamento e execução da Action de salvamento
        # ----------------------------------------------------
        t_ato_save_action = TAtoSaveAction()
        ato_response = t_ato_save_action.execute(t_ato_save_schema)

        # ----------------------------------------------------
        # Grava histórico de inclusão do ato
        # ----------------------------------------------------
        now = datetime.now()
        now_br = now.strftime("%d/%m/%Y %H:%M:%S")
        usuario_id = t_ato_save_schema.usuario_id
        ato_id = getattr(ato_response, "ato_id", t_ato_save_schema.ato_id)

        historico_schema = THistoricoSaveSchema(
            tabela="T_ATO",
            campo="Cadastro de novo ato",
            operacao="I",
            new_value=None,
            usuario_id=usuario_id,
            data=now,
            id=ato_id,
            observacao=f"Ato cadastro pelo usuário({usuario_id}), no dia {now_br}",
            data_registro=None,
            dados_complementares=None,
        )

        t_historico_save_service = THistoricoSaveService()
        t_historico_save_service.execute(historico_schema)

        return ato_response
