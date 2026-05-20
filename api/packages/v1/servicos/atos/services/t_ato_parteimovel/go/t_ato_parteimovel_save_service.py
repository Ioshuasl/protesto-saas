from datetime import datetime

from packages.v1.servicos.atos.actions.t_ato_parteimovel.t_ato_parteimovel_save_action import (
    TAtoParteImovelSaveAction,
)
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaSchema
from packages.v1.servicos.atos.schemas.t_historico_schema import THistoricoSaveSchema
from packages.v1.servicos.atos.schemas.t_ato_parteimovel_schema import (
    TAtoParteImovelSaveSchema,
)
from packages.v1.servicos.atos.services.t_historico.go.t_historico_save_service import (
    THistoricoSaveService,
)
from packages.v1.sequencia.services.g_sequencia.generate_service import GenerateService


class TAtoParteImovelSaveService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de criação de registros na tabela T_ATO_PARTEIMOVEL.
    """

    def execute(self, t_ato_parteimovel_save_schema: TAtoParteImovelSaveSchema):
        """
        Executa a operação de salvamento do registro no banco de dados.

        Args:
            t_ato_parteimovel_save_schema (TAtoParteImovelSaveSchema):
                O esquema com os dados a serem salvos.

        Returns:
            O registro recém-criado.
        """

        # ----------------------------------------------------
        # Geração automática de ID (sequência)
        # ----------------------------------------------------
        if not t_ato_parteimovel_save_schema.ato_parteimovel_id:
            # Cria o schema de sequência
            sequencia_schema = GSequenciaSchema()
            sequencia_schema.tabela = "T_ATO_PARTEIMOVEL"

            # Gera a sequência atualizada
            generate = GenerateService()
            sequencia = generate.execute(sequencia_schema)

            # Atualiza o ID no schema
            t_ato_parteimovel_save_schema.ato_parteimovel_id = sequencia.sequencia

        # ----------------------------------------------------
        # Instanciamento e execução da Action de salvamento
        # ----------------------------------------------------
        t_ato_parteimovel_save_action = TAtoParteImovelSaveAction()
        ato_parteimovel_response = t_ato_parteimovel_save_action.execute(
            t_ato_parteimovel_save_schema
        )

        # ----------------------------------------------------
        # Grava histórico de inclusão da parte/imóvel
        # ----------------------------------------------------
        now = datetime.now()
        now_br = now.strftime("%d/%m/%Y %H:%M:%S")
        usuario_id = t_ato_parteimovel_save_schema.usuario_id
        ato_parteimovel_id = getattr(
            ato_parteimovel_response,
            "ato_parteimovel_id",
            t_ato_parteimovel_save_schema.ato_parteimovel_id,
        )

        historico_schema = THistoricoSaveSchema(
            tabela="T_ATO_PARTEIMOVEL",
            campo="Cadastro de parte/imóvel",
            operacao="I",
            new_value=None,
            usuario_id=usuario_id,
            data=now,
            id=ato_parteimovel_id,
            observacao=f"Parte/imóvel cadastrado pelo usuário({usuario_id}), no dia {now_br}",
            data_registro=None,
            dados_complementares=None,
        )

        t_historico_save_service = THistoricoSaveService()
        t_historico_save_service.execute(historico_schema)

        return ato_parteimovel_response
